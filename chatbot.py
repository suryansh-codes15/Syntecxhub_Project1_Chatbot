import time
import re
from pathlib import Path

# ========== VERSION BANNER ==========
print("=== PROJECT 1 CHATBOT v1.1 (Syntecx) ===")

# Path for chat history (ensures folder-safe handling)
HISTORY_FILE = Path("chat_history.txt")


# --------- Conversation Logger ---------
def log_message(message: str) -> None:
    """Append a single line to chat_history.txt with UTF-8 encoding."""
    try:
        with HISTORY_FILE.open("a", encoding="utf-8") as f:
            f.write(message + "\n")
    except OSError:
        # Silent fail for logging so chatbot still works even if file issue
        pass


# --------- Helper functions ---------
def contains_any(text: str, keywords) -> bool:
    """Return True if any keyword is present as a substring in text."""
    text = text.lower()
    return any(k in text for k in keywords)


def is_greeting(text: str) -> bool:
    """
    Detect greeting as a full word, not as part of another word.
    Example:
      'hi' -> greeting
      'hi there' -> greeting
      'scholarship' -> NOT greeting
    """
    greetings = ["hi", "hii", "hiii", "hello", "hey"]
    words = re.findall(r"\b\w+\b", text.lower())
    return any(word in greetings for word in words)


def is_empty(text: str) -> bool:
    """Check if the user input is empty or only spaces."""
    return text.strip() == ""


# --------- Response Logic / Rules ---------
def generate_response(user_input: str) -> str:
    text = user_input.lower().strip()

    # 0. Empty input
    if is_empty(user_input):
        return "Please type something about admission, fees, hostel, courses, etc."

    # 1. Greeting intent
    if is_greeting(text):
        return (
            "Hi! I am your PROJECT 1 college info chatbot. "
            "You can ask about admission, fees, courses, hostel, placements, scholarships, etc."
        )

    # 2. Help intent
    if any(phrase in text for phrase in ["help", "what can you do", "options"]):
        return (
            "I can answer questions about:\n"
            "- admission / applying / registration\n"
            "- courses and branches\n"
            "- fees and scholarships\n"
            "- hostel and campus facilities\n"
            "- placements and internships\n"
            "Just type a keyword like 'admission', 'fees', 'hostel', 'placement', 'scholarship' etc."
        )

    # 3. Small talk
    if "how are you" in text:
        return "I'm running perfectly for your internship project! How are you doing?"
    if contains_any(text, ["thank", "thanks", "thx"]):
        return "You're welcome! 😊"
    if "who are you" in text:
        return "I am a simple rule-based chatbot created as your AI internship Project 1."

    # 4. Domain knowledge (college-related)

    # Admission-related
    if contains_any(
        text,
        [
            "admission",
            "admit",
            "apply",
            "application",
            "enroll",
            "enrollment",
            "registration",
            "register",
        ],
    ):
        return (
            "The admission process usually includes:\n"
            "1) Filling the online/offline application form\n"
            "2) Appearing for the entrance exam / counseling (if required)\n"
            "3) Submitting documents for verification\n"
            "4) Paying the initial admission fee.\n"
            "For exact dates and requirements, please check the official college website."
        )

    # Courses / branches
    if contains_any(
        text,
        [
            "course",
            "courses",
            "branch",
            "branches",
            "program",
            "programs",
            "department",
            "stream",
        ],
    ):
        return (
            "Common courses offered include B.Tech (various branches), BCA, BBA, MBA and more.\n"
            "Different colleges may have branches like CSE, IT, ECE, ME, CE, etc.\n"
            "Check the course list on the college website for exact details."
        )

    # Fees
    if contains_any(
        text, ["fee", "fees", "tuition", "college fee", "semester fee", "sem fee"]
    ):
        return (
            "The fee structure depends on the course and year.\n"
            "Generally, there are tuition fees, exam fees, and hostel fees (if applicable).\n"
            "For the latest and accurate fee details, refer to the official fee structure or admission brochure."
        )

    # Hostel / accommodation
    if contains_any(text, ["hostel", "accommodation", "room", "mess", "pg"]):
        return (
            "Many colleges provide hostel facilities with separate hostels for boys and girls.\n"
            "Hostels often include mess, Wi-Fi, security, and basic facilities.\n"
            "You should contact the hostel office or see the website for room availability and charges."
        )

    # Scholarship / financial help
    if contains_any(
        text, ["scholarship", "scholarships", "fee waiver", "financial aid"]
    ):
        return (
            "Scholarships are usually available based on merit, category, or government schemes.\n"
            "Students can also apply for state and central government scholarships.\n"
            "Contact the scholarship or accounts section for eligibility and application procedure."
        )

    # Placements / jobs
    if contains_any(
        text,
        [
            "placement",
            "placements",
            "package",
            "salary",
            "job",
            "jobs",
            "campus drive",
            "campus placement",
        ],
    ):
        return (
            "The training and placement cell helps students with internships and final placements.\n"
            "Companies visit the campus for recruitment drives, offering various job roles and packages.\n"
            "You can check the college placement report or talk to the T&P cell for more details."
        )

    # Internships
    if contains_any(text, ["intern", "interns", "internship", "internships"]):
        return (
            "Internships are an important part of practical learning.\n"
            "Students are encouraged to do internships in companies during semester breaks.\n"
            "The placement cell / department often shares internship opportunities and guides students on how to apply."
        )

    # Campus / facilities
    if contains_any(text, ["campus", "facility", "facilities", "infrastructure"]):
        return (
            "Most college campuses include classrooms, labs, libraries, hostels, sports grounds, canteen, and Wi-Fi.\n"
            "Facilities vary from college to college, so it’s best to check the official website or visit the campus."
        )

    # Library
    if contains_any(text, ["library", "books", "reading room"]):
        return (
            "The college library generally provides textbooks, reference books, journals, and a quiet reading area.\n"
            "Students can issue books using their library card or ID as per the library rules."
        )

    # Canteen / food
    if contains_any(text, ["canteen", "food", "mess food"]):
        return (
            "The campus canteen / mess provides meals and snacks for students.\n"
            "Quality and variety of food may differ, but basic veg and non-veg options are usually available."
        )

    # Timing / contact
    if contains_any(text, ["timing", "time", "office hours", "working hours"]):
        return (
            "College and office timings are usually from morning to afternoon.\n"
            "For exact timings, please check the notice, website, or contact the college office."
        )

    if contains_any(text, ["contact", "phone", "email", "number"]):
        return (
            "You can contact the college through the official phone number, email, "
            "or contact form given on the website.\n"
            "Look for the 'Contact Us' page on the official site."
        )

    # 5. Default fallback response
    return (
        "I'm not sure about that.\n"
        "Try asking using small keywords like:\n"
        "- admission / apply\n"
        "- courses / branches\n"
        "- fees / scholarship\n"
        "- hostel / campus\n"
        "- placement / internship\n"
        "- library / canteen / contact."
    )


# --------- Main Chat Loop ---------
def chat() -> None:
    print("Chatbot: Hi! I am your PROJECT 1 rule-based college info chatbot.")
    print("Chatbot: Type 'exit' to end the chat.\n")

    while True:
        user_input = input("You: ")

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Exit condition first (do not log empty accidental exit lines as user queries)
        if user_input.lower().strip() in ["exit", "quit"]:
            bot_reply = "Goodbye! Chat history is saved in chat_history.txt."
            print("Chatbot:", bot_reply)
            log_message(f"[{timestamp}] You: {user_input}")
            log_message(f"[{timestamp}] Chatbot: {bot_reply}")
            break

        # Log user message
        log_message(f"[{timestamp}] You: {user_input}")

        # Generate bot reply
        bot_reply = generate_response(user_input)
        print("Chatbot:", bot_reply)

        # Log bot reply
        log_message(f"[{timestamp}] Chatbot: {bot_reply}")


if __name__ == "__main__":
    chat()
