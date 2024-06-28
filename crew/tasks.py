from crewai import Task
from crew.agents import expanded_biography_generator_agent, creative_theme_generator_agent, song_creation_agent, song_evaluation_agent, song_editor_agent, music_description_agent
from crew.tools import file_read_tool, directory_read_tool, write2file_tool
from textwrap import dedent

# Paths
expanded_biography_output_path = f'data/output/expanded_musician_biography.txt'
generated_themes_path = f'data/output/generated_themes.txt'
generated_song_path = f'data/output/generated_song.txt'
song_evaluation_report_path = f'data/output/song_evaluation_report.txt'
corrected_song_path = f'data/output/corrected_song.txt'
music_description_output_path = f'data/output/music_description.txt'

task_expanded_biography_generation = Task(
    description=dedent("""    
        - **Scopo**: 
          - Generare una biografia estesa in ITALIANO a partire dalla breve biografia fornita: {topic}.

        - **Obiettivo**:
          - Produrre una biografia completa che includa il nome d'arte del musicista, interessi unici, successi passati, stile musicale e altre informazioni di background.

        - **Dettagli da Includere**:
          - **Nome d'Arte**: Inventare un nome d'arte distintivo se non fornito.
          - **Genere**: Descrivere lo stile musicale o il genere del musicista.
          - **Sesso**: Specificare il sesso del musicista se non fornito.
          - **Interessi**: Documentare hobby insoliti, passioni e influenze che distinguono il musicista.
          - **Successi Passati**: Evidenziare traguardi unici nella carriera del musicista.
          - **Informazioni di Background**: Fornire una storia personale e professionale intrigante.

        - **Esempi**:
          - Nome d'Arte: "Maestro"
          - Genere: "Musica elettronica con un tocco di influenze classiche."
          - Sesso: "Maschio"
          - Interessi: "Colleziona sintetizzatori vintage, ispirato dai romanzi di fantascienza."
          - Successi Passati: "Ha composto la colonna sonora per un film indie premiato."
          - Informazioni di Background: "Nato nel 1985, ha iniziato a suonare il theremin all'età di 7 anni."
    """),
    
    expected_output=dedent(f"""
        Una biografia dettagliata ed estesa del musicista in ITALIANO, che copre:
          - Interessi unici, successi passati e altre informazioni di background rilevanti.
        La biografia dovrebbe essere completa, dettagliata e fornire una comprensione completa della vita e della carriera del musicista.
        La risposta non deve contenere altre parole oltre a quelle richieste.
        """),
    agent=expanded_biography_generator_agent,
    tools=[],
    output_file=expanded_biography_output_path
)

task_creative_theme_generation = Task(
    description=dedent(f"""    
        - **Scopo**: 
          - Generare in ITALIANO un tema creativo e articolato e una trama narrativa per la canzone basata sulla biografia estesa fornita in "{expanded_biography_output_path}". 
          Lo scopo è far partecipare la canzone al festival di Sanremo.
          Nel caso in cui siano presenti dei temi tra i tag [TEMA] e [/TEMA], devi assolutamente aderire ad essi per creare il tema della canzone.
          [TEMA]{{theme}}[/TEMA]
          

        - **Obiettivo**:
          - Produrre un tema unico e immaginativo per una canzone che catturi l'essenza dello stile del musicista senza riferimenti diretti alla biografia.
          - Essere originali e creativi, evitare i cliché e garantire che i temi siano coinvolgenti e freschi.

        - **Dettagli da Includere**:
          - **Tema**: Creare un tema e una narrativa inventivi che possano essere utilizzati nella canzone.
          - **Ispirazione**: Trarre ispirazione dalla biografia del musicista ma garantire un distacco creativo.

        - **Esempi**:
          - Tema: "La storia di una penna che scrive senza intervento umano". Genere: "Elettronica con vibrazioni anni '80".
          - Tema: "Esplorare il cosmo per trovare il suono dell'universo." Genere: "Ambient con elementi sperimentali".
          - Tema: "Un uomo che comunica con le piante". Genere: "Folk acustico con un tocco di psichedelia".
          - Tema: "Storia d'amore ironica tra un robot e un umano". Genere: "Synth-pop con un tocco retro-futuristico".
          - Tema: "Visione ironica della situazione politica italiana". Genere: "Rap con un tocco di satira".
    """),
    
    expected_output=dedent(f"""
        Un tema creativo unico e una trama narrativa per la canzone, ispirati dalla biografia del musicista, insieme al genere. Dovrebbe essere scritto in ITALIANO.
        Il tema dovrebbe essere unico, coinvolgente e fornire una prospettiva fresca per la canzone.
        La risposta non deve contenere altre parole oltre a quelle richieste.
        """),
    agent=creative_theme_generator_agent,
    tools=[file_read_tool, directory_read_tool],
    output_file=generated_themes_path
)

task_song_creation = Task(
    description=dedent(f"""    
        - **Scopo**: 
          - Creare una canzone originale e di alta qualità in ITALIANO, emulando lo stile del musicista basato sul tema fornito in "{generated_themes_path}". Lo scopo è far partecipare la canzone al festival di Sanremo.

        - **Obiettivo**:
          - Produrre una canzone che catturi l'essenza dello stile del musicista senza riferimenti diretti alla biografia, garantendo che sia fresca, coinvolgente e priva di cliché.

        - **Dettagli da Includere**:
          - **Stile**: Emulare lo stile musicale unico del musicista.
          - **Temi**: Incorporare i temi creativi e le narrazioni forniti.
          - **Originalità**: Garantire che i testi siano originali e evitare frasi ripetitive e banali. E' ammesso che i ritornelli siano uguali.
          - **Coinvolgimento**: Creare testi che siano avvincenti e mantengano l'interesse dell'ascoltatore per tutta la durata.
          - **Fantasia**: Non citare il genere musicale, non citare clichè, non citare la biografia, non basarsi su frasi fatte e su luoghi comuni.
        - **Struttura**:
          La canzone dovrebbe avere una struttura chiara che includa strofe, ritornelli e bridge, seguendo una narrazione coerente. Utilizzare tag come [VERSE], [CHORUS], [BRIDGE], [SPECIAL], [OUTRO], ecc., per delineare le diverse sezioni.
    """),
    expected_output=dedent(f"""
        Una canzone in ITALIANO che emuli accuratamente lo stile del musicista e incorpori i temi creativi forniti. 
        La canzone dovrebbe essere originale, di alta qualità e riflettere la voce artistica unica del musicista senza cadere nei cliché.
        La risposta non deve contenere altre parole oltre a quelle richieste.
    """),
    agent=song_creation_agent,
    tools=[file_read_tool, directory_read_tool],
    output_file=generated_song_path
)

task_song_evaluation = Task(
    description=dedent(f"""    
        - **Scopo**: 
          - Valutare la canzone generata descritta in "{generated_song_path}" per determinare se necessita di miglioramenti. Lo scopo è far partecipare la canzone al festival di Sanremo.

        - **Obiettivo**:
          - Valutare la qualità dei testi della canzone, concentrandosi su potenziali problemi e aree di miglioramento.

        - **Dettagli da Valutare**:
          - **Monotonia**: Verificare la presenza di elementi ripetitivi o monotoni nei testi. E' ammesso che i ritornelli siano uguali.
          - **Qualità**: Valutare la qualità complessiva dei testi, includendo:
            - **Liricità**: Analizzare la creatività e la qualità poetica dei testi.
            - **Profondità**: Valutare la profondità emotiva e tematica dei testi.
            - **Coesione**: Assicurarsi che i testi formino una narrativa o un tema coerente e consistente.
            - **Originalità**: Valutare l'unicità e l'originalità dei testi. Non deve esser epresente il genere musicale, la biografia, frasi fatte o luoghi comuni.
            - **Immagini**: Verificare l'uso di immagini vivide ed evocative.
            - **Chiarezza**: Assicurarsi che i testi siano chiari e facilmente comprensibili.
            - **Rilevanza**: Valutare se i testi sono pertinenti al messaggio o al tema della canzone.
            - **Coinvolgimento**: Determinare se i testi sono coinvolgenti e capaci di catturare l'attenzione dell'ascoltatore.
            - **Pacing**: Verificare il flusso e il ritmo dei testi, assicurando un buon equilibrio tra strofe e ritornelli.
            - **Grammatica e Sintassi**: Identificare eventuali errori grammaticali o frasi goffe.
            - **Schema di Rima**: Valutare la coerenza e la creatività dello schema di rima.
            - **Coerenza**: Assicurarsi che il tono e lo stile rimangano coerenti per tutta la canzone. Tutti i ritornelli devono essere uguali.
    """),
    expected_output=dedent(f"""
        Un rapporto di valutazione dettagliato della canzone generata.
        Il rapporto dovrebbe includere raccomandazioni specifiche per miglioramenti.
        Non sono ammessi giudizi generici o vaghi; le critiche devono essere costruttive e mirate a migliorare la qualità della canzone.
        Devono essere riportate le frasi problematiche o le sezioni che richiedono modifiche. Devono essere indicati gli errori grammaticali e devono essere suggerite correzioni.
    """),
    agent=song_evaluation_agent,
    tools=[file_read_tool, directory_read_tool],
    output_file=song_evaluation_report_path
)

task_song_editing = Task(
    description=dedent(f"""    
        - **Scopo**: 
          - Modificare la canzone generata descritta in "{generated_song_path}" basandosi sul rapporto di valutazione in "{song_evaluation_report_path}". Lo scopo è far partecipare la canzone al festival di Sanremo.

        - **Obiettivo**:
          - Migliorare la canzone affrontando i problemi o le carenze identificate durante la valutazione.
          - Assicurare la correttezza grammaticale e la coerenza stilistica.
          - Tutti i ritornelli devono essere uguali.
          - Aggiungi i giusti accenti tonici in italiano su tutte le parole, per esempio "alcuno" diventa "alcùno", "oblio" diventa "oblìo", "maestro" diviene "maèstro", "brindisi" diventa "brìndisi". Aggiungili solo se sicuro.

    """),
    
    expected_output=dedent(f"""
        Una versione corretta della canzone che affronti i problemi identificati nel rapporto di valutazione.
        La canzone finale dovrebbe essere coinvolgente, di alta qualità e riflettere lo stile unico del musicista.
        La risposta non deve contenere altre parole oltre a quelle richieste.
    """),
    agent=song_editor_agent,
    tools=[file_read_tool, directory_read_tool],
    output_file=corrected_song_path
)

task_generate_music_description = Task(
    description=dedent(f"""
        - **Scopo**: 
          - Creare una breve e coinvolgente descrizione dell'arrangiamento musicale per la canzone generata basata sulla biografia del musicista in "{expanded_biography_output_path}" e i testi della canzone in "{corrected_song_path}". Lo scopo è far partecipare la canzone al festival di Sanremo.

        - **Obiettivo**:
          - Produrre una descrizione dell'arrangiamento musicale in un massimo di 120 caratteri. In inglese.

        - **Dettagli da Includere**:
          - Catturare l'essenza dello stile della canzone e il suo impatto emotivo.
          - Incorporare elementi chiave dalla biografia del musicista e dai testi della canzone.
          - Tipo di voce (indica sempre se maschile o femminile)

        - **Esempi**:
          - "A soulful pop ballad blending classical influences with synths. 90s sounds. Female voice"
          - "Energetic rock anthem, distortion, rough male voice."
    """),
    
    expected_output=dedent(f"""
        Una descrizione concisa dell'arrangiamento musicale in un massimo di 120 caratteri in INGLESE. La descrizione dovrebbe essere coinvolgente e riflettere accuratamente lo stile e l'essenza della canzone generata. Lo scopo è far partecipare la canzone al festival di Sanremo.
        La risposta non deve contenere altre parole oltre a quelle richieste.
    """),
    agent=music_description_agent,
    tools=[file_read_tool, directory_read_tool],
    output_file=music_description_output_path
)
