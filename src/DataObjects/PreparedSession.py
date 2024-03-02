import json


class PreparedSession:
    def __init__(self, mean_absolute_diff_timestamps=0.0,
                 mean_absolute_diff_amount=0.0, median_longitude_latitude=(0.0, 0.0),
                 median_target_ip="", median_dest_ip=""):
        self.mean_absolute_diff_timestamps = mean_absolute_diff_timestamps
        self.mean_absolute_diff_amount = mean_absolute_diff_amount
        self.median_longitude_latitude = median_longitude_latitude
        self.median_target_ip = median_target_ip
        self.median_dest_ip = median_dest_ip

    def __str__(self):
        return f"Mean Absolute Diff Timestamps: {self.mean_absolute_diff_timestamps}\n" \
               f"Mean Absolute Diff Amount: {self.mean_absolute_diff_amount}\n" \
               f"Median Longitude|Latitude: {self.median_longitude_latitude}\n" \
               f"Median TargetIP: {self.median_target_ip}\n" \
               f"Median DestIP: {self.median_dest_ip}"
    def to_json(self):
        return {
            "mean_absolute_diff_timestamps": self.mean_absolute_diff_timestamps,
            "mean_absolute_diff_amount": self.mean_absolute_diff_amount,
            "median_longitude_latitude": list(self.median_longitude_latitude),
            "median_target_ip": self.median_target_ip,
            "median_dest_ip": self.median_dest_ip
        }
