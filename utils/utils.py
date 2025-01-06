from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Define a mapping from note type string to their corresponding descriptions
NOTE_TYPE_DESCRIPTORS = {
    "Action Items": "List any actionable tasks, assignments, or follow-ups identified during the conversation.",
    "Brainstorming Ideas": "Provide a summary of the creative ideas and brainstorming session, highlighting key suggestions.",
    "Client Meeting Recap": "Summarize the key points discussed during the client meeting, including important topics, decisions, or outcomes.",
    "Decision Summary": "Summarize the key decisions made during the meeting and their implications.",
    "Executive Summary": "Provide a high-level overview of the meeting, summarizing the main points and key takeaways.",
    "Feedback Summary": "Summarize the feedback given during the session, highlighting key points and suggestions.",
    "Financial Overview": "Provide a summary of the financial discussion, including key metrics, trends, and financial decisions.",
    "Follow-Up Tasks": "Identify the tasks and follow-ups that were assigned during the meeting.",
    "Key Points": "Highlight the most important points discussed in the conversation.",
    "Meeting Minutes": "Provide detailed meeting minutes, capturing all significant points, decisions, and action items.",
    "Negotiation Outcomes": "Summarize the outcomes of the negotiation, including agreements, compromises, and next steps.",
    "Performance Review Notes": "Summarize key points from the performance review, including feedback and areas for improvement.",
    "Project Planning Notes": "Provide an overview of the project planning session, including timelines, responsibilities, and key objectives.",
    "Risk Assessment": "Summarize the risk assessment discussion, highlighting identified risks and proposed mitigation strategies.",
    "Sales Call Summary": "Summarize the key points from the sales call, including client needs, objections, and next steps.",
    "Strategy Outline": "Provide an outline of the strategy discussed, including main objectives and planned actions.",
    "SWOT Analysis": "Provide an analysis of Strengths, Weaknesses, Opportunities, and Threats discussed during the meeting.",

    # Educational
    "Abstract Summary": "Provide an abstract summary of the main topics discussed.",
    "Action Plan for Improvement": "Outline an action plan for improvement based on the discussion.",
    "Concept Maps": "Summarize the key concepts discussed and their relationships.",
    "Debate Highlights": "Summarize the main arguments and counterarguments from the debate.",
    "Flashcards": "Highlight key terms and concepts that can be turned into flashcards for study purposes.",
    "Important Dates and Deadlines": "List important dates and deadlines discussed.",
    "Key Terms and Definitions": "Summarize the key terms and their definitions as discussed.",
    "Lab Results Summary": "Provide a summary of the lab results and their implications.",
    "Lecture Notes": "Summarize the lecture notes, highlighting the main points and key takeaways.",
    "Parent-Teacher Conference Summary": "Summarize the main points discussed during the parent-teacher conference.",
    "Problem-Solving Steps": "Outline the problem-solving steps discussed during the session.",
    "Q&A Highlights": "Highlight key questions and answers from the session.",
    "Study Guide": "Summarize key topics and concepts that can be used as a study guide.",

    # Personal
    "Budget and Financial Notes": "Summarize the budget and financial notes discussed.",
    "Counseling Insights": "Provide insights from the counseling session.",
    "Creative Ideas List": "Summarize the creative ideas discussed.",
    "Daily Planner": "Summarize key points for daily planning.",
    "Family Meeting Notes": "Summarize the main points discussed during the family meeting.",
    "Goal Tracker": "Summarize the goals discussed and any progress updates.",
    "Gratitude List": "List items discussed for gratitude.",
    "Health and Wellness Log": "Summarize health and wellness points discussed.",
    "Mind Mapping": "Provide a summary of the mind mapping session.",
    "Personal Reflections": "Summarize personal reflections shared during the session.",
    "Score Tracking": "Summarize any score tracking discussed.",
    "Story Outline": "Provide an outline of the story discussed.",
    "Vacation Itinerary": "Summarize the vacation itinerary discussed.",

    # General
    "Agenda Outline": "Provide an outline of the agenda.",
    "Detailed Analysis": "Provide a detailed analysis of the discussion.",
    "FAQs": "Summarize frequently asked questions discussed.",
    "Lessons Learned": "Summarize the lessons learned from the discussion.",
    "Motivational Points": "Summarize the motivational points discussed.",
    "Next Steps": "Identify the next steps to be taken.",
    "Priorities List": "Summarize the priorities discussed.",
    "Pros and Cons List": "List the pros and cons discussed.",
    "Resource List": "Provide a list of resources mentioned.",
    "Summary for Different Audiences": "Provide a summary tailored for different audiences."
}
