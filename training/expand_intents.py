
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CATALOG_PATH = (
    PROJECT_ROOT / "data" / "training" / "intent_catalog.json"
)

NEW_INTENTS = {
    0: {
        "leave_notice_period": [
            "How early should I apply for planned leave?",
            "What is the minimum notice for vacation?",
            "Can I submit a leave request one day before?",
            "How many working days in advance is leave required?",
            "Is advance notice mandatory for planned leave?"
        ],
        "leave_portal_access": [
            "Where can I access the employee leave portal?",
            "Which system is used to request time off?",
            "How do I open the HR leave application system?",
            "Where should I log in to submit vacation?",
            "Is there an online portal for leave requests?"
        ],
        "leave_request_status": [
            "How can I check whether my leave was approved?",
            "Where can I see my pending leave requests?",
            "How do I track a submitted vacation request?",
            "Can I check the status of my leave application?",
            "My leave request is pending. How can I follow up?"
        ],
        "unplanned_absence": [
            "I cannot come to work today due to an emergency.",
            "What should I do if I am unexpectedly absent?",
            "How should I inform my manager about sudden absence?",
            "I am unable to attend work without prior notice.",
            "What is the procedure for reporting an unplanned absence?"
        ]
    },
    1: {
        "laptop_connectivity": [
            "My company laptop cannot connect to WiFi.",
            "What should I do when my office laptop loses internet?",
            "I cannot access the network from my work computer.",
            "My corporate laptop keeps disconnecting from WiFi.",
            "How can I get help with laptop network issues?"
        ],
        "software_error": [
            "A company application keeps crashing.",
            "How do I report an error in workplace software?",
            "My business application is not responding.",
            "Who can help when an installed program fails?",
            "I receive an error whenever I open a work application."
        ],
        "remote_access": [
            "How can I access company systems while working remotely?",
            "I need help connecting to corporate resources from home.",
            "What should I do if remote access stops working?",
            "How do employees connect to internal systems remotely?",
            "I cannot reach company applications outside the office."
        ],
        "ticket_status": [
            "How can I check the progress of my IT ticket?",
            "Where can I see updates on my helpdesk request?",
            "My technical support request is still unresolved.",
            "How do I follow up on an open IT incident?",
            "Can I track the status of my support ticket?"
        ]
    },
    2: {
        "client_meal_claim": [
            "Can I claim a meal purchased during a client meeting?",
            "Are approved client lunch expenses reimbursable?",
            "How do I request reimbursement for a business dinner?",
            "Does the company cover meals with clients?",
            "What is the policy for claiming client entertainment meals?"
        ],
        "transport_claim": [
            "Can I claim transportation costs for client visits?",
            "Are approved business taxi fares reimbursable?",
            "How do I submit a claim for work-related transport?",
            "Does the company reimburse travel between client offices?",
            "What transport expenses qualify for reimbursement?"
        ],
        "claim_rejection": [
            "What should I do if my reimbursement claim is rejected?",
            "Why might an expense request be declined?",
            "Who should I contact about a denied expense claim?",
            "Can I correct an expense report that was rejected?",
            "How can I follow up on an unsuccessful reimbursement?"
        ],
        "expense_submission": [
            "Where do I submit my business expense report?",
            "How can I file a reimbursement request?",
            "What is the process for submitting approved expenses?",
            "How do employees send expense claims for processing?",
            "Which system should I use for expense reimbursement?"
        ]
    },
    3: {
        "booking_changes": [
            "How can I modify an existing business travel booking?",
            "What should I do if my approved flight changes?",
            "Can I update my corporate travel reservation?",
            "Who handles changes to company travel bookings?",
            "How do I reschedule an official business trip?"
        ],
        "domestic_travel": [
            "What rules apply to travel within the country?",
            "How should employees arrange domestic business trips?",
            "Are there specific requirements for domestic travel?",
            "What company policy applies to local business flights?",
            "How do I plan an approved domestic work trip?"
        ],
        "hotel_booking": [
            "How do I reserve a hotel for business travel?",
            "Where should I book accommodation for a company trip?",
            "Can employees choose their own business hotels?",
            "What is the process for booking approved accommodation?",
            "How should I arrange lodging for an official trip?"
        ],
        "travel_itinerary": [
            "Where can I find my business travel itinerary?",
            "How do I check my upcoming corporate travel details?",
            "Who can help me confirm my official trip schedule?",
            "How can I review my travel booking information?",
            "Where should I verify my business trip arrangements?"
        ]
    }
}


def main():
    with open(CATALOG_PATH, "r", encoding="utf-8") as file:
        catalog = json.load(file)

    added = 0

    for category in catalog["categories"]:
        label = category["label"]

        existing_ids = {
            intent["id"]
            for intent in category["intents"]
        }

        for intent_id, queries in NEW_INTENTS[label].items():
            if intent_id in existing_ids:
                print(f"Skipping existing intent: {intent_id}")
                continue

            category["intents"].append({
                "id": intent_id,
                "queries": queries
            })

            added += 1

    with open(CATALOG_PATH, "w", encoding="utf-8") as file:
        json.dump(
            catalog,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(f"New intents added: {added}")
    print("Intent catalog updated successfully.")


if __name__ == "__main__":
    main()
