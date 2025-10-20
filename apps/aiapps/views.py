from django.shortcuts import render
from .models import SalesAnalysis
import pandas as pd
from prophet import Prophet
import skfuzzy as fuzz
import numpy as np
import os
from django.conf import settings
from datetime import datetime, timezone

# Path to the CSV file in the aiapps folder
DATA_SOURCE = os.path.join(settings.BASE_DIR, 'apps', 'aiapps', 'shvr.csv')

def get_file_modified_time(file_path):
    """Get the last modified time of the file in UTC."""
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)

def calculate_sales_analysis(df):
    """Calculate all sales analysis metrics from the dataframe."""
    # Monthly Sales Trends
    monthly_sales_trends = df['Total_SS'].resample('ME').sum()
    monthly_sales_data = {
        'labels': monthly_sales_trends.index.strftime('%Y-%m').tolist(),
        'data': monthly_sales_trends.values.tolist()
    }

    # Top 10 Most Selling Products
    most_selling_products = df.groupby('ItemName')['Total_SS'].sum().sort_values(ascending=False).head(10)
    top_products_data = {
        'labels': most_selling_products.index.tolist(),
        'data': most_selling_products.values.tolist()
    }

    # Prophet model for sales forecast
    total_monthly_sales = df['Total_SS'].resample('ME').sum().reset_index()
    total_monthly_sales.columns = ['ds', 'y']
    total_model = Prophet(yearly_seasonality=True, daily_seasonality=False)
    total_model.fit(total_monthly_sales)
    future_dates = total_model.make_future_dataframe(periods=12, freq='ME')
    total_forecast = total_model.predict(future_dates)

    # Sales Forecast Data
    sales_forecast_data = {
        'labels': total_forecast['ds'].dt.strftime('%Y-%m').tolist(),
        'predicted': total_forecast['yhat'].tolist(),
        'upper': total_forecast['yhat_upper'].tolist(),
        'lower': total_forecast['yhat_lower'].tolist()
    }

    # Fuzzy Logic Demand Classification
    item_type_sales_freq = df.groupby('ItemTypeName')['Total_SS'].sum().reset_index()
    max_quantity = max(item_type_sales_freq['Total_SS'])
    x_freq = np.linspace(0, max_quantity, 100)
    very_high_freq = fuzz.trimf(x_freq, [max_quantity/2, max_quantity, max_quantity])
    high_freq = fuzz.trimf(x_freq, [max_quantity/4, max_quantity/2, max_quantity*3/4])
    medium_freq = fuzz.trimf(x_freq, [max_quantity/8, max_quantity/4, max_quantity/2])
    low_freq = fuzz.trimf(x_freq, [0, 0, max_quantity/4])

    def classify_demand(freq):
        very_high = fuzz.interp_membership(x_freq, very_high_freq, freq)
        high = fuzz.interp_membership(x_freq, high_freq, freq)
        medium = fuzz.interp_membership(x_freq, medium_freq, freq)
        low = fuzz.interp_membership(x_freq, low_freq, freq)
        if very_high > max(high, medium, low):
            return 'Very High'
        elif high > max(very_high, medium, low):
            return 'High'
        elif medium > max(very_high, high, low):
            return 'Medium'
        else:
            return 'Low'

    item_type_sales_freq['DemandLevel'] = item_type_sales_freq['Total_SS'].apply(classify_demand)
    demand_data = {
        'labels': item_type_sales_freq['ItemTypeName'].tolist(),
        'data': item_type_sales_freq['DemandLevel'].tolist()
    }

    # Category-wise Sales Prediction
    category_forecasts = {}
    category_monthly_data = df.groupby('ItemTypeName')['Total_SS'].resample('ME').sum().reset_index()

    for category in category_monthly_data['ItemTypeName'].unique():
        category_data = category_monthly_data[
            category_monthly_data['ItemTypeName'] == category
        ][['SalesDate', 'Total_SS']]
        category_data.columns = ['ds', 'y']

        if len(category_data) < 24:  # Ensure there is enough data for forecasting
            continue

        # Fit the Prophet model
        model = Prophet(yearly_seasonality=True, daily_seasonality=False)
        model.fit(category_data)

        # Forecast future sales
        future_dates = model.make_future_dataframe(periods=12, freq='ME')
        forecast = model.predict(future_dates)

        # Store forecasted values in the dictionary
        category_forecasts[category] = {
            'dates': forecast['ds'].dt.strftime('%Y-%m').tolist(),
            'yhat': forecast['yhat'].tolist(),
            'yhat_upper': forecast['yhat_upper'].tolist(),
            'yhat_lower': forecast['yhat_lower'].tolist(),
            'historical_sales': category_data['y'].tolist()
        }

    return {
        'monthly_sales_data': monthly_sales_data,
        'top_products_data': top_products_data,
        'sales_forecast_data': sales_forecast_data,
        'demand_data': demand_data,
        'category_forecasts': category_forecasts
    }

def ai_dashboard(request):
    try:
        # Try to get existing analysis
        analysis = SalesAnalysis.objects.get(pk=1)
        
        # Check if data source file exists
        if not os.path.exists(DATA_SOURCE):
            raise FileNotFoundError("Data source file not found")
        
        # Get file's last modified time
        file_modified_time = get_file_modified_time(DATA_SOURCE)
        
        # Check if data is stale (file was modified after last analysis update)
        if file_modified_time > analysis.last_updated:
            print(f"Data is stale. File modified: {file_modified_time}, Last update: {analysis.last_updated}")
            raise SalesAnalysis.DoesNotExist  # Trigger recalculation
            
        print("Using cached analysis data")
            
    except (SalesAnalysis.DoesNotExist, FileNotFoundError) as e:
        print(f"Calculating new analysis data. Reason: {str(e)}")
        
        try:
            # Load and preprocess data
            df = pd.read_csv(DATA_SOURCE, low_memory=False)
            
            # Basic validation of the data
            if df.empty:
                raise ValueError("Data file is empty")
                
            # Preprocess the dataframe
            df['SalesDate'] = pd.to_datetime(df['SalesDate'], errors='coerce')
            df = df[df['SalesDate'] < '2024-06-01']
            df['TotalGistPrice'] = pd.to_numeric(df['TotalGistPrice'], errors='coerce')
            df['DiscountInPercentage'] = pd.to_numeric(df['DiscountInPercentage'], errors='coerce')
            df['Quantity_SS'] = pd.to_numeric(df['Quantity_SS'], errors='coerce')
            df['UnitPrice_SS'] = pd.to_numeric(df['UnitPrice_SS'], errors='coerce')
            df.dropna(subset=['Total_SS'], inplace=True)
            df.set_index('SalesDate', inplace=True)

            # Calculate all metrics
            analysis_data = calculate_sales_analysis(df)
            
            # Update or create the analysis record
            analysis, created = SalesAnalysis.objects.update_or_create(
                pk=1,  # Use a fixed primary key
                defaults=analysis_data
            )
            
            print(f"{'Created' if created else 'Updated'} analysis data")
            
        except Exception as e:
            print(f"Error during calculation: {str(e)}")
            raise  # Re-raise the exception to be caught by outer try-except

    except Exception as e:
        # Log the error and return a graceful error response
        print(f"Error processing sales analysis: {str(e)}")
        return render(request, 'aiapps/error.html', {'error_message': str(e)})

    # Prepare context with cached or newly calculated data
    context = {
        'monthly_sales_data': analysis.monthly_sales_data,
        'top_products_data': analysis.top_products_data,
        'sales_forecast_data': analysis.sales_forecast_data,
        'demand_data': analysis.demand_data,
        'category_forecasts': analysis.category_forecasts,
        'last_updated': analysis.last_updated
    }

    return render(request, 'aiapps/dashboard.html', context)