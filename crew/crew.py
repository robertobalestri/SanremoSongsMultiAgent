from crewai import Crew, Process
from crew.agents import expanded_biography_generator_agent, creative_theme_generator_agent, song_creation_agent, song_evaluation_agent, song_editor_agent, music_description_agent
from crew.tasks import task_expanded_biography_generation,  task_creative_theme_generation, task_song_creation, task_song_evaluation, task_song_editing, task_generate_music_description
from crew.llms import azure_llm_4_turbo_low_temperature
import os


# Instantiate your crew with a sequential process
main_crew = Crew(
    agents=[expanded_biography_generator_agent, creative_theme_generator_agent, song_creation_agent, song_evaluation_agent, song_editor_agent, music_description_agent],  
    tasks=[task_expanded_biography_generation, task_creative_theme_generation, task_song_creation, task_song_evaluation, task_song_editing, task_generate_music_description], 
    verbose=2,  # You can set it to 1 or 2 to different logging levels
    process=Process.sequential,
    cache=True,
    share_crew=False,
    manager_llm=azure_llm_4_turbo_low_temperature,
    function_calling_llm=azure_llm_4_turbo_low_temperature
)
