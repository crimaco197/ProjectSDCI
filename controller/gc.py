import os
import time
import threading
from prometheus_api_client import PrometheusConnect

# Analyze function
def analyze():
    print("Analyze")
    time.sleep(1)

# Plan function
def plan():
    print("Plan")
    time.sleep(1)

# Execute functions for blocking/unblocking
def execute_block():
    """
    Applies the AuthorizationPolicy to block zones.
    """
    print("Blocking zone2 and zone3 using AuthorizationPolicy...")
    os.system("kubectl apply -f config-blockZones/deny-zones_on_z2_z3.yaml")
    print("Block policy applied.")

def execute_unblock():
    """
    Removes the AuthorizationPolicy to unblock zones.
    """
    print("Unblocking zone2 and zone3 (removing AuthorizationPolicy)...")
    os.system("kubectl delete -f config-blockZones/deny-zones_on_z2_z3.yaml --ignore-not-found")
    print("Block policy removed.")

# Monitor class
class Monitor(threading.Thread):
    """
    Monitors Prometheus metrics in a background thread.
    Alerts are raised when the response time exceeds a threshold.
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.alerts = 0
        self.running = True
        self.prometheus = PrometheusConnect(url="http://localhost:9090", disable_ssl=True)
        self.response_time_history = []

    def get_response_time(self):
        """
        Queries the 95th percentile response time from Prometheus.
        Returns the numeric value or None if no data.
        """
        query = (
        #    'histogram_quantile(0.95, '
        #    'sum(rate(istio_request_duration_milliseconds_bucket'
        #    '{app="iot-zone1", connection_security_policy="unknown", destination_app="iot-gateway"}[5m])) by (le))'
        'histogram_quantile(0.95, sum(rate(istio_request_duration_milliseconds_bucket[5m])) by (le))'
        )
        result = self.prometheus.custom_query(query)
        if result:
            return float(result[0]['value'][1])
        return None

    def run(self):
        while self.running:
            response_time = self.get_response_time()
            self.response_time_history.append(response_time)
            if len(self.response_time_history) > 5:  # Keep last 5 measurements
                self.response_time_history.pop(0)

            print(f"Current response time: {response_time} ms")
            # If response time is above 500 ms, raise an alert
            if response_time and response_time > 50:
                self.alerts += 1
                print(f"ALERT! High response time: {response_time} ms")
            time.sleep(5)

    def stop(self):
        self.running = False

def main():
    monitor = Monitor()
    monitor.start()

    is_blocked = False  # Tracks whether the AuthorizationPolicy is active
    consecutive_normal = 0  # Tracks consecutive cycles with normal response times

    try:
        while True:
            # If no alerts, evaluate if it's time to unblock
            if monitor.alerts == 0:
                if is_blocked:
                    # Check if response time has been normal for 3 consecutive cycles
                    if all(rt and rt < 50 for rt in monitor.response_time_history):
                        consecutive_normal += 1
                        if consecutive_normal >= 3:
                            # If stable for 3 cycles, unblock
                            analyze()
                            plan()
                            print("Execute UNBLOCK")
                            execute_unblock()
                            is_blocked = False
                            consecutive_normal = 0
                    else:
                        # Reset the counter if any response time is high
                        consecutive_normal = 0
                time.sleep(2)
            else:
                # There is at least one alert
                if not is_blocked:
                    # Block if not already blocked
                    analyze()
                    plan()
                    print("Execute BLOCK")
                    execute_block()
                    is_blocked = True

                # Reduce alert count to indicate we've handled it
                monitor.alerts -= 1
                time.sleep(2)

    except KeyboardInterrupt:
        print("Shutting down monitor...")

    monitor.stop()
    monitor.join()

if __name__ == "__main__":
    main()