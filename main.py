import time

class PaymentStateMachine:
    # Define all possible states for a payment
    STATES = {
        "PENDING",      # Initial state, waiting for processing
        "PROCESSING",   # Payment is being processed by a gateway
        "COMPLETED",    # Payment was successful
        "FAILED",       # Payment failed (e.g., card declined, insufficient funds)
        "REFUNDED",     # Payment was successfully refunded
        "CANCELLED"     # Payment was cancelled before completion
    }

    # Define valid transitions between states
    # Key: current state, Value: set of allowed next states
    TRANSITIONS = {
        "PENDING": {"PROCESSING", "CANCELLED"},
        "PROCESSING": {"COMPLETED", "FAILED"},
        "COMPLETED": {"REFUNDED"},
        "FAILED": {"PENDING", "CANCELLED"}, # FAILED can retry (PENDING) or be cancelled
        "REFUNDED": set(), # Terminal state, no further transitions
        "CANCELLED": set() # Terminal state, no further transitions
    }

    def __init__(self, initial_state="PENDING"):
        if initial_state not in self.STATES:
            raise ValueError(f"Invalid initial state: {initial_state}")
        self._current_state = initial_state
        print(f"Payment initialized. Current state: {self.current_state}")

    @property
    def current_state(self):
        return self._current_state

    def transition_to(self, new_state):
        if new_state not in self.STATES:
            print(f"Error: Invalid state '{new_state}' requested.")
            return False

        # Check if the requested transition is valid from the current state
        if new_state in self.TRANSITIONS.get(self._current_state, set()):
            print(f"Transitioning from '{self._current_state}' to '{new_state}'...")
            self._current_state = new_state
            print(f"Current state: {self.current_state}")
            return True
        else:
            print(f"Error: Invalid transition from '{self._current_state}' to '{new_state}'.")
            return False

# --- Example Usage ---
if __name__ == "__main__":
    print("\n--- Scenario 1: Successful Payment Flow ---")
    payment1 = PaymentStateMachine() # Starts in PENDING

    # Simulate payment processing
    payment1.transition_to("PROCESSING") # PENDING -> PROCESSING
    time.sleep(0.5)
    payment1.transition_to("COMPLETED")  # PROCESSING -> COMPLETED

    print("\n--- Scenario 2: Failed Payment then Retry ---")
    payment2 = PaymentStateMachine()

    # Simulate a failed payment attempt
    payment2.transition_to("PROCESSING")
    time.sleep(0.5)
    payment2.transition_to("FAILED")     # PROCESSING -> FAILED

    # Attempt an invalid transition (e.g., directly to COMPLETED from FAILED)
    payment2.transition_to("COMPLETED")  # This should fail

    # Retry the payment by moving back to PENDING
    payment2.transition_to("PENDING")    # FAILED -> PENDING (to retry)
    payment2.transition_to("PROCESSING") # PENDING -> PROCESSING
    time.sleep(0.5)
    payment2.transition_to("COMPLETED")  # PROCESSING -> COMPLETED

    print("\n--- Scenario 3: Payment Cancellation ---")
    payment3 = PaymentStateMachine()

    # User cancels before processing starts
    payment3.transition_to("CANCELLED") # PENDING -> CANCELLED

    # Attempt an invalid transition from CANCELLED (terminal state)
    payment3.transition_to("PROCESSING") # This should fail

    print("\n--- Scenario 4: Refund ---")
    payment4 = PaymentStateMachine()
    payment4.transition_to("PROCESSING")
    payment4.transition_to("COMPLETED")
    time.sleep(0.5)
    payment4.transition_to("REFUNDED") # COMPLETED -> REFUNDED

    # Attempt an invalid transition from REFUNDED (terminal state)
    payment4.transition_to("COMPLETED") # This should fail
