from django.db import models

class SalesAnalysis(models.Model):
    monthly_sales_data = models.JSONField()
    top_products_data = models.JSONField()
    sales_forecast_data = models.JSONField()
    demand_data = models.JSONField()
    category_forecasts = models.JSONField(null=True, blank=True)  # Allow null values
  # New field for category-wise forecasts
    last_updated = models.DateTimeField(auto_now=True)

    def is_data_stale(self, data_source):
        import os
        last_modified = os.path.getmtime(data_source)
        return last_modified > self.last_updated.timestamp()
