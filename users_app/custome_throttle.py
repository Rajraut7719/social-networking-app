from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import Throttled

class LoginThrottle(UserRateThrottle):
    scope = 'login'

    def throttle_failure(self):
        wait = int(self.wait())  # Convert to integer
        
        # Convert wait time to minutes, and seconds
        minutes = (wait % 3600) // 60
        seconds = wait % 60
        
        # Create the custom message
        detail = f"Too many login attempts. Please try again {minutes} minutes, and {seconds} seconds."
        raise Throttled(detail=detail)
