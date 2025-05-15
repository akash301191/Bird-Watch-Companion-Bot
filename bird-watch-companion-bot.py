import tempfile
import streamlit as st

from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat
from agno.tools.serpapi import SerpApiTools

from textwrap import dedent

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def render_bird_profile():
    st.markdown("---")
    col1, col2 = st.columns(2)

    # Column 1: Image Upload
    with col1:
        st.subheader("📸 Upload Bird Image")
        uploaded_image = st.file_uploader(
            "Choose a photo of the bird you spotted",
            type=["jpg", "jpeg", "png"]
        )

    # Column 2: Location + Additional Input
    with col2:
        st.subheader("🗺️ Bird Sighting Details")

        region = st.text_input(
            "Where did you spot the bird?",
            placeholder="e.g., Central Park, NY or Western Ghats"
        )

        behavior = st.text_input(
            "Describe the bird's behavior (optional)",
            placeholder="e.g., hopping on the ground, flying in circles, feeding"
        )

    return {
        "uploaded_image": uploaded_image,
        "region": region,
        "behavior": behavior if behavior else "Not Specified",
    }

def generate_bird_report(bird_profile):
    uploaded_image = bird_profile["uploaded_image"]
    region = bird_profile["region"]
    behavior = bird_profile["behavior"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_image.getvalue())
        image_path = tmp.name

    # Step 1: Bird Identifier
    bird_identifier = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="Bird Species Identifier",
        role="Identifies bird species from an uploaded image and provides scientific and common names, visual traits, and confidence.",
        description=(
            "You are a bird identification expert. Given an image of a bird, you will analyze physical characteristics such as plumage, beak shape, markings, and posture "
            "to identify the most likely bird species. You also return a brief natural history summary."
        ),
        instructions=[
            "Carefully analyze the uploaded bird image.",
            "Identify the most likely bird species using visible traits.",
            "Return the common name, scientific name (italicized), confidence level (as a %), and list of key visual traits.",
            "Include a short paragraph describing how these traits relate to the species.",
            "Format output using markdown like this:\n\n"
            "**Common Name**: <Name>\n"
            "**Scientific Name**: *<Botanical Name>*\n"
            "**Confidence**: <Percentage>\n"
            "**Visual Traits**:\n- <Trait 1>\n- <Trait 2>\n\n<Short paragraph>",
            "If unsure, suggest 2-3 most probable matches and clearly note uncertainty."
        ],
        markdown=True
    )

    identifier_response = bird_identifier.run(
        f"Identify this bird based on visual characteristics. Region: {region}. Observed behavior: {behavior}.",
        images=[Image(filepath=image_path)]
    )
    bird_identification = identifier_response.content

    # Step 2: Bird Behavior & Care Research
    bird_researcher = Agent(
        name="Bird Habitat Researcher",
        role="Searches for habitat, diet, and migration patterns of a given bird species using region-specific data.",
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a birdwatching and wildlife ecology researcher. Based on the identified bird species and location,
            construct a focused web search to find behavioral, feeding, nesting, and migration info from reliable sources.
        """),
        instructions=[
            "Take the bird's common and scientific name and location into account.",
            "Create a highly focused Google search query (e.g., 'Barn Swallow migration and diet North America').",
            "Use `search_google` with that query.",
            "Return 10 of the most relevant links in a markdown bullet list.",
            "Exclude ads, duplicates, and generic sites. Do not summarize content."
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        add_datetime_to_instructions=True,
        markdown=True
    )

    research_response = bird_researcher.run(bird_identification)
    bird_links = research_response.content

    # Step 3: Birdwatching & Habitat Report
    bird_advisor = Agent(
        name="Birdwatching Guide Generator",
        role="Generates a comprehensive markdown report with species identification, ecological traits, birdwatching insights, and conservation notes.",
        model=OpenAIChat(id="o3-mini", api_key=st.session_state.openai_api_key),
        description = dedent("""
            You are a birdwatching and habitat care advisor. You are given:
            1. A structured bird identification summary, including common name, scientific name, visual traits, and confidence level.
            2. A list of URLs from trusted sources that explain the bird’s feeding behavior, migration patterns, nesting habits, and conservation status.

            Your job is to produce a well-formatted Markdown report with two main sections:
            - ## 🐦 Bird Identification
            - ## 🌍 Observation & Care Guide
        """),
        instructions=[
            "Start with ## 🐦 Bird Identification",
            "Include the following:\n"
            "- **Common Name**\n"
            "- **Scientific Name** (italicized)\n"
            "- **Confidence** (percentage)\n"
            "- **Visual Traits** (bullet list describing key field markings)\n"
            "- A **concise paragraph** summarizing species highlights and distinctive features",
            "",
            "Then create a ## 🌍 Observation & Care Guide with these sections:",
            "",
            "### 🍽️ Feeding Habits",
            "- Describe the bird’s diet: insects, seeds, berries, fish, nectar, etc.",
            "- Include **how** it forages (e.g., ground feeder, mid-canopy, diving, aerial).",
            "- Mention seasonal or migratory diet changes if relevant.",
            "",
            "### 🪶 Behavior & Activity",
            "- Detail flight patterns, vocalizations, social behavior (solitary or flocking).",
            "- Include info on territoriality, courtship, or notable mating displays.",
            "- Highlight **migratory behavior** and general movement patterns if known.",
            "",
            "### 📍 Habitat & Nesting",
            "- Describe preferred ecosystems (e.g., wetlands, grasslands, forests, coasts).",
            "- Mention typical nest location (tree cavity, reed beds, cliffs, etc.).",
            "- Include egg count, material preferences, and seasonal nesting timeline if known.",
            "",
            "### 🚨 Conservation Notes",
            "- Provide IUCN status or regional protection status (e.g., Least Concern, Endangered).",
            "- Highlight any population trends, known threats (habitat loss, hunting, climate impact), or ongoing conservation efforts.",
            "- Mention if the species is protected under local acts or listed migratory treaties.",
            "",
            "### 📚 Recommended Resources",
            "- From the provided list of URLs, choose 5–10 high-quality sources.",
            "- Present each as a clean Markdown link: [Resource Title](URL).",
            "- Prioritize educational, government, or ornithological sources (e.g., Audubon, BirdLife, Cornell Lab).",
            "",
            "🧠 **Important Guidelines**:",
            "- Extract accurate information only from the given URLs—do NOT fabricate or assume any information.",
            "- Avoid generic filler. Be descriptive, engaging, and informative like a naturalist field guide.",
            "- Use Markdown headings and lists. Never include raw links or explanation about the tool itself.",
            "- Output should be beautifully structured and professional enough for birdwatchers or educators."
        ],
        markdown=True,
        add_datetime_to_instructions=True
    )

    final_prompt = f"""
    Bird Identification Summary:
    {bird_identification}

    Research Links:
    {bird_links}

    Use these to create a full birdwatching and habitat care guide.
    """

    report_response = bird_advisor.run(final_prompt)
    bird_report = report_response.content

    return bird_report

def main() -> None:
    # Page config
    st.set_page_config(page_title="Bird Watch Companion Bot", page_icon="🐦", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🐦 Bird Watch Companion Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Spot and identify birds through your camera lens, and receive personalized care, feeding, and migration guidance.",
        unsafe_allow_html=True
    )

    render_sidebar()
    bird_profile = render_bird_profile()
    
    st.markdown("---")

    # Trigger Report Generation
    if st.button("🐦 Generate Bird Report"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        elif "uploaded_image" not in bird_profile or not bird_profile["uploaded_image"]:
            st.error("Please upload a bird image before generating the report.")
        else:
            with st.spinner("Identifying the bird and generating a personalized habitat and behavior guide..."):
                report = generate_bird_report(bird_profile)
                st.session_state.bird_report = report
                st.session_state.image = bird_profile["uploaded_image"]

    # Display and download the report
    if "bird_report" in st.session_state:
        st.markdown("## 🖼️ Uploaded Bird Image")
        st.image(st.session_state.image, use_container_width=False)

        st.markdown(st.session_state.bird_report, unsafe_allow_html=True)

        st.download_button(
            label="📥 Download Bird Report",
            data=st.session_state.bird_report,
            file_name="birdwatch_report.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    main()
