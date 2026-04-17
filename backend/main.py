# Deployment Trigger: 2026-04-17 11:01
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
import os
import sys
import io

# Ensure UTF-8 output on Windows to prevent UnicodeEncodeError
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = FastAPI(title="Swasthya Sahayak Edge AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryContext(BaseModel):
    text: str
    language: str = "en"

# --- FULL REGIONAL TRANSLATIONS DB ---
# Added exhaustive support for Hindi, Marathi, Tamil, and Telugu for ALL categories.

vector_db = {
    "heart": {
        "keywords": ["heart", "cardiac", "collapse", "chest pain", "दिल", "हृदय", "छातीत", "இதயம்", "గుండె"],
        "protocols": {
            "English": "1. Check for responsiveness and breathing. 2. If unresponsive, call 108 and begin CPR immediately. 3. Push hard and fast in the center of the chest (100-120 bpm).",
            "Hindi": "1. प्रतिक्रिया और सांस की जांच करें। 2. यदि कोई प्रतिक्रिया नहीं है, तो 108 पर कॉल करें और तुरंत CPR शुरू करें। 3. छाती के केंद्र में जोर से और तेजी से दबाएं (100-120 प्रति मिनट)।",
            "Marathi": "1. प्रतिसाद आणि श्वासाची तपासणी करा. 2. प्रतिसाद नसल्यास, १०८ ला कॉल करा आणि त्वरित CPR सुरू करा. 3. छातीच्या मध्यभागी जोरात आणि वेगाने दाब द्या (१००-१२० प्रति मिनिट).",
            "Tamil": "1. எதிர்வினை மற்றும் சுவாசத்தை சரிபார்க்கவும். 2. பதில் இல்லை என்றால், 108 ஐ அழைத்து உடனடியாக CPR ஐத் தொடங்கவும். 3. நெஞ்சின் மையத்தில் வேகமாகவும் பலமாகவும் அழுத்தவும்.",
            "Telugu": "1. ప్రతిస్పందన మరియు శ్వాసను తనిఖీ చేయండి. 2. ప్రతిస్పందన లేకపోతే, 108 కి కాల్ చేసి వెంటనే CPR ప్రారంభించండి. 3. ఛాతీ మధ్యలో బలంగా మరియు వేగంగా నొక్కండి."
        },
        "level": "CRITICAL LEVEL 5", "color": "#ef4444", "isEmerg": True, "sysText": "Auto-dialing Ambulance...", "visual": "/img/heart.png"
    },
    "snake": {
        "keywords": ["snake", "cobra", "viper", "bite", "सांप", "साप", "பாம்பு", "పాము"],
        "protocols": {
            "English": "1. Keep the person calm and completely still to slow venom spread. 2. Immobilize the bitten limb; do NOT apply a tourniquet. 3. Transport to a hospital immediately.",
            "Hindi": "1. व्यक्ति को शांत रखें और जहर फैलने से रोकने के लिए स्थिर रखें। 2. काटे गए अंग को हिलाएं नहीं; पट्टी न बांधें। 3. तुरंत अस्पताल ले जाएं।",
            "Marathi": "1. व्यक्तीला शांत ठेवा आणि विष पसरू नये म्हणून पूर्णपणे स्थिर ठेवा. 2. जखम झालेला भाग हालवू नका; टूर्निकेट लावू नका. 3. त्वरित रुग्णालयात घेऊन जा.",
            "Tamil": "1. நபர் அமைதியாகவும் அசையாமலும் இருப்பதை உறுதி செய்யவும். 2. கடித்த பகுதியை அசையாமல் வைக்கவும்; கட்டுகளை இறுக்க வேண்டாம். 3. உடனடியாக மருத்துவமனைக்கு அழைத்துச் செல்லவும்.",
            "Telugu": "1. వ్యక్తిని ప్రశాంతంగా మరియు కదలకుండా ఉంచండి. 2. కరిచిన భాగాన్ని కదలకుండా ఉంచండి; గట్టిగా కట్టవద్దు. 3. వెంటనే ఆసుపత్రికి తీసుకెళ్లండి."
        },
        "level": "CRITICAL LEVEL 5", "color": "#ef4444", "isEmerg": True, "sysText": "Dispatching GPS...", "visual": "/img/snake.png"
    },
    "burn": {
        "keywords": ["burn", "fire", "scald", "जलना", "भाजणे", "தீக்காயம்", "కాలిన", "కాలుట"],
        "protocols": {
            "English": "1. Cool the burn immediately under running cool water for 20 minutes. 2. Do not use ice, butter, or toothpaste. 3. Cover loosely with clean cloth.",
            "Hindi": "1. जले हुए हिस्से पर 20 मिनट तक ठंडा पानी डालें। 2. बर्फ या टूथपेस्ट न लगाएं। 3. साफ कपड़े से ढीला ढक दें।",
            "Marathi": "1. भाजलेल्या भागावर २० मिनिटे थंड पाणी टाका. 2. बर्फ किंवा टूथपेस्ट वापरू नका. 3. स्वच्छ कापडाने सैल झाकून ठेवा.",
            "Tamil": "1. காயத்தை 20 நிமிடங்கள் குளிர்ந்த நீரில் நனைக்கவும். 2. ஐஸ் அல்லது பேஸ்ட் பயன்படுத்த வேண்டாம். 3. சுத்தமான துணியால் லேசாக மூடவும்.",
            "Telugu": "1. కాలిన చోట 20 నిమిషాల పాటు చల్లటి నీటిని పోయండి. 2. ఐస్ లేదా టూత్ పేస్ట్ రాయవద్దు. 3. శుభ్రమైన గుడ్డతో కప్పండి."
        },
        "level": "URGENT LEVEL 3", "color": "#f59e0b", "isEmerg": False, "sysText": "Monitoring Situation...", "visual": "/img/burn.png"
    },
    "stroke": {
        "keywords": ["stroke", "paralyzed", "slurred", "droop", "लकवा", "स्ट्रोक", "पक्षाघात", "பக்கவாதம்", "పక్షవాతం"],
        "protocols": {
            "English": "1. Think FAST: Face drooping, Arm weakness, Speech difficulty, Time to call 108. 2. Keep the person calm. 3. Do not give food or drink.",
            "Hindi": "1. FAST याद रखें: चेहरा लटकना, हाथ की कमजोरी, बोलने में कठिनाई, 108 पर कॉल करने का समय। 2. व्यक्ति को शांत रखें। 3. कुछ भी खाने-पीने को न दें।",
            "Marathi": "1. FAST लक्षात ठेवा: चेहरा वाकडा होणे, हाताचा कमकुवतपणा, बोलण्यात अडथळा, १०८ ला कॉल करण्याची वेळ. 2. व्यक्तीला शांत ठेवा. 3. खाण्यास किंवा पिण्यास काहीही देऊ नका।",
            "Tamil": "1. FAST ஐ நினையுங்கள்: முகம் கோணுதல், கை தளர்ச்சி, பேச்சுத் தடுமாற்றம், 108 ஐ அழைக்க வேண்டிய நேரம். 2. நபரை அமைதியாக வைத்திருக்கவும். 3. உணவு அல்லது পানীয় வழங்க வேண்டாம்.",
            "Telugu": "1. FAST గుర్తుంచుకోండి: ముఖం వంకరపోవడం, చేయి బలహీనత, మాట తడబడటం, 108కి కాల్ చేయాల్సిన సమయం. 2. వ్యక్తిని ప్రశాంతంగా ఉంచండి. 3. ఆహారం లేదా పానీయం ఇవ్వవద్దు."
        },
        "level": "CRITICAL LEVEL 5", "color": "#ef4444", "isEmerg": True, "sysText": "Dispatching GPS...", "visual": "/img/stroke.png"
    },
    "seizure": {
        "keywords": ["seizure", "fit", "convulsion", "दौरा", "फिट", "अपस्मार", "வலிப்பு", "ఫిట్స్"],
        "protocols": {
            "English": "1. Clear the area of hard or sharp objects. 2. Do not hold them down or put anything in their mouth. 3. Place them in the recovery position after the seizure stops.",
            "Hindi": "1. आस-पास से कठोर या नुकीली चीजें हटा दें। 2. उन्हें पकड़ें नहीं और मुंह में कुछ भी न डालें। 3. दौरा खत्म होने के बाद उन्हें करवट पर लिटाएं।",
            "Marathi": "1. आजूबाजूच्या कडक किंवा अणकुचीदार वस्तू दूर करा. 2. त्यांना दाबून धरू नका किंवा तोंडात काहीही घालू नका. 3. फिट थांबल्यानंतर त्यांना एका कुशीवर वळवून झोपवा।",
            "Tamil": "1. கடினமான அல்லது கூர்மையான பொருட்களை அப்புறப்படுத்துங்கள். 2. அவர்களை அழுத்திப் பிடிக்காதீர்கள் அல்லது வாயில் எதையும் வைக்காதீர்கள். 3. வலிப்பு நின்ற பிறகு அவர்களை ஒருக்களித்துப் படுக்க வைக்கவும்.",
            "Telugu": "1. గట్టి లేదా పదునైన వస్తువులను చుట్టుపక్కల నుండి తొలగించండి. 2. వారిని గట్టిగా పట్టుకోవద్దు లేదా నోటిలో ఏమీ పెట్టవద్దు. 3. ఫిట్స్ ఆగిపోయిన తర్వాత వారిని ఒక పక్కకు తిప్పి పడుకోబెట్టండి."
        },
        "level": "CRITICAL LEVEL 5", "color": "#ef4444", "isEmerg": True, "sysText": "Monitoring Situation...", "visual": "/img/seizure.png"
    },
    "poison": {
        "keywords": ["poison", "toxic", "swallowed", "जहर", "विष", "நஞ்சு", "విషం"],
        "protocols": {
            "English": "1. Do NOT induce vomiting. 2. Do not give food or drink. 3. Find the container and call 108 immediately.",
            "Hindi": "1. उल्टी न कराएं। 2. कुछ भी खाने-पीने को न दें। 3. जहर का डब्बा ढूंढें और तुरंत 108 पर कॉल करें।",
            "Marathi": "1. उलट्या करण्याचा प्रयत्न करू नका. 2. खाण्यास किंवा पिण्यास काहीही देऊ नका. 3. विषाचा डबा शोधा आणि त्वरित १०८ ला कॉल करा।",
            "Tamil": "1. வாந்தியைத் தூண்ட வேண்டாம். 2. உணவு அல்லது பானம் கொடுக்க வேண்டாம். 3. விஷம் இருந்த கொள்கலனைக் கண்டுபிடித்து உடனடியாக 108 ஐ அழைக்கவும்.",
            "Telugu": "1. వాంతులు చేయించవద్దు. 2. ఆహారం లేదా పానీయం ఇవ్వవద్దు. 3. విషం ఉన్న డబ్బాను వెతికి వెంటనే 108కి కాల్ చేయండి."
        },
        "level": "CRITICAL LEVEL 5", "color": "#ef4444", "isEmerg": True, "sysText": "Dispatching GPS...", "visual": "/img/poison.png"
    },
    "choking": {
        "keywords": ["choking", "choke", "stuck", "दम", "घसा", "மூச்சுத்திணறல்", "ఉక్కిరిబిక్కిరి"],
        "protocols": {
            "English": "1. Give 5 firm back blows. 2. Give 5 abdominal thrusts (Heimlich). 3. Repeat until the object is dislodged.",
            "Hindi": "1. पीठ पर 5 बार जोर से थपथपाएं। 2. पेट पर 5 बार दबाव डालें (हीमलिच)। 3. जब तक वस्तु बाहर न निकल जाए, तब तक दोहराएं।",
            "Marathi": "1. पाठीवर ५ जोरात फटके द्या. 2. पोटावर ५ वेळा दाब द्या (Heimlich). 3. जोपर्यंत वस्तू बाहेर येत नाही तोपर्यंत पुन्हा करा।",
            "Tamil": "1. முதுகில் 5 முறை பலமாகத் தட்டவும். 2. அடிவயிற்றில் 5 முறை அழுத்தம் கொடுக்கவும் (ஹெய்ம்லிச்). 3. பொருள் வெளியேறும் வரை மீண்டும் செய்யவும்.",
            "Telugu": "1. వెనుక భాగంలో 5 సార్లు గట్టిగా కొట్టండి. 2. పొత్తికడుపుపై 5 సార్లు ఒత్తిడి ఇవ్వండి (హీమ్లిచ్). 3. అడ్డుపడిన వస్తువు బయటకు వచ్చే వరకు పునరావృతం చేయండి."
        },
        "level": "CRITICAL LEVEL 5", "color": "#ef4444", "isEmerg": True, "sysText": "Dispatching GPS...", "visual": "/img/choking.png"
    },
    "bleeding": {
        "keywords": ["bleeding", "blood", "cut", "wound", "रक्त", "खून", "இரத்தம்", "రక్తం"],
        "protocols": {
            "English": "1. Apply direct, firm pressure with a clean cloth. 2. Do not remove the cloth if soaked; add more on top. 3. Call 108 if bleeding is severe.",
            "Hindi": "1. साफ कपड़े से घाव पर सीधा दबाव डालें। 2. यदि कपड़ा भीग जाए, तो उसे हटाएं नहीं; ऊपर से और कपड़ा रखें। 3. यदि खून ज्यादा बह रहा हो, तो 108 पर कॉल करें।",
            "Marathi": "1. स्वच्छ कापडाने जखमेवर थेट आणि जोरात दाब द्या. 2. कापड रक्ताने भिजल्यास ते काढू नका; त्यावर दुसरे कापड ठेवा. 3. रक्तस्त्राव थांबत नसल्यास १०८ ला कॉल करा।",
            "Tamil": "1. சுத்தமான துணியால் நேரடியாகவும் பலமாகவும் அழுத்தம் கொடுக்கவும். 2. துணி நனைந்துவிட்டால் அதை எடுக்க வேண்டாம்; அதன் மேல் இன்னும் துணிகளை வைக்கவும். 3. இரத்தப்போக்கு அதிகமாக இருந்தால் 108 ஐ அழைக்கவும்.",
            "Telugu": "1. శుభ్రమైన గుడ్డతో నేరుగా, గట్టిగా ఒత్తిడిని కలిగించండి. 2. గుడ్డ పూర్తిగా తడిసిపోతే దాన్ని తొలగించవద్దు; దానిపై మరొక గుడ్డను ఉంచండి. 3. రక్తస్రావం ఎక్కువగా ఉంటే 108కి కాల్ చేయండి."
        },
        "level": "CRITICAL LEVEL 5", "color": "#ef4444", "isEmerg": True, "sysText": "Dispatching GPS...", "visual": "/img/bleeding.png"
    },
    "fracture": {
        "keywords": ["fracture", "broken", "bone", "limb", "leg", "arm", "हड्डी", "पैर", "हाथ", "टूटना", "फ्रैक्चर", "मोच", "हाड", "எலும்பு முறிவு", "ముక్కలు", "ఎముక"],
        "protocols": {
            "English": "1. Immobilize the injured area using a splint or sling. 2. Apply ice packs to reduce swelling (not directly on skin). 3. Seek medical help immediately and do not try to realign the bone.",
            "Hindi": "1. स्प्लिंट या स्लिंग का उपयोग करके घायल हिस्से को स्थिर करें। 2. सूजन कम करने के लिए बर्फ लगाएं (सीधे त्वचा पर नहीं)। 3. तुरंत चिकित्सा सहायता लें और हड्डी को खुद जोड़ने की कोशिश न करें।",
            "Marathi": "1. स्प्लिंट किंवा स्लिंग वापरून जखमी भाग स्थिर करा. 2. सूज कमी करण्यासाठी बर्फ लावा (थेट त्वचेवर नाही). 3. त्वरित वैद्यकीय मदत घ्या आणि हाड स्वतः जोडण्याचा प्रयत्न करू नका.",
            "Tamil": "1. ஒரு பிளெண்ட் அல்லது ஸ்லிங்கைப் பயன்படுத்தி காயம் அடைந்த பகுதியை அசையாமல் வைக்கவும். 2. வீக்கத்தைக் குறைக்க ஐஸ் பேக்குகளைப் பயன்படுத்துங்கள். 3. உடனடியாக மருத்துவ உதவியை நாடவும்.",
            "Telugu": "1. స్ప్లింట్ లేదా స్లింగ్‌ని ఉపయోగించి గాయపడిన భాగాన్ని కదలకుండా ఉంచండి. 2. వాపును తగ్గించడానికి ఐస్ ప్యాక్‌లను వేయండి. 3. వెంటనే వైద్య సహాయం తీసుకోండి."
        },
        "level": "URGENT LEVEL 3", "color": "#f59e0b", "isEmerg": False, "sysText": "Analyzing Situation...", "visual": "/img/generic.png"
    }
}

# --- PDF KNOWLEDGE FALLBACK ---
KNOWLEDGE_FILE = "knowledge_base.json"
pdf_knowledge = {}
if os.path.exists(KNOWLEDGE_FILE):
    with open(KNOWLEDGE_FILE, 'r', encoding='utf-8') as f:
        pdf_knowledge = json.load(f)

def retrieve_rag_context(query: str):
    query = query.lower()
    best_match = None
    best_score = 0
    
    for key, data in vector_db.items():
        score = sum(5 if kw in query else 0 for kw in data["keywords"])
        if score > best_score:
            best_score = score
            best_match = data
            
    if best_match and best_score >= 5:
        return best_match

    combined_kb = "\n".join(pdf_knowledge.values()).split('\n')
    search_terms = [w for w in query.split() if len(w) >= 2 and w not in {'what', 'should', 'doing', 'where', 'when', 'how', 'someone'}]
    print(f"DEBUG: query='{query}' search_terms={search_terms}")
    
    scored_snippets = []
    for line in combined_kb:
        line_clean = line.lower()
        score = sum(10 if kw in line_clean else 0 for kw in search_terms)
        if score >= 10 and len(line) > 50:
            scored_snippets.append((score, line.strip()))
            
    scored_snippets.sort(key=lambda x: x[0], reverse=True)
    print(f"DEBUG: found {len(scored_snippets)} snippets")
    if scored_snippets:
        # Clean 'h' artifacts from snippets
        clean_snippets = [s[1].replace('\th', '').replace('h ', '').strip() for s in scored_snippets[:3]]
        return {
            "keywords": [],
            "snippets": clean_snippets,
            "level": "URGENT LEVEL 3", "color": "#f59e0b", "isEmerg": False, 
            "sysText": "Analyzing Manuals...", "visual": "/img/generic.png"
        }

    return {
        "keywords": [],
        "protocols": {"English": "1. Assess the situation and check for breathing. 2. Keep the person calm. 3. Call 108 if condition worsens."},
        "level": "CAUTION LEVEL 2", "color": "#3b82f6", "isEmerg": False, "sysText": "Analyzing Query...", "visual": "/img/generic.png"
    }

def ask_medllama(query: str, context: str, target_lang: str = "English", force_format: bool = False):
    if target_lang == "English" and not force_format: return context
    
    if force_format:
        prompt = f"""Task: Synthesize a first aid protocol for '{query}' using the provided context.
Context: {context}
Language: {target_lang}
Format: ONLY output 3 numbered steps starting with '1. '. Be concise. No filler."""
    else:
        prompt = f"""Task: Translate this medical protocol into {target_lang}.
Context: {context}
Format: ONLY output 2-3 numbered steps starting with '1. '. No filler."""
    
    payload = {"model": "llama3.1:latest", "prompt": prompt, "stream": False, "options": {"temperature": 0.1, "num_predict": 100}}
    try:
        res = requests.post("http://localhost:11434/api/generate", json=payload, timeout=60)
        return res.json().get("response", context).strip()
    except:
        return context

@app.post("/api/triage")
def triage_engine(query: QueryContext):
    context_data = retrieve_rag_context(query.text)
    
    # Check if we have a hardcoded translation for this language
    lang_key = query.language.strip()
    if "protocols" in context_data and lang_key in context_data["protocols"]:
        llm_output = context_data["protocols"][lang_key]
    else:
        # Fallback to LLM for formatting or translation
        if "snippets" in context_data:
            base_context = " ".join(context_data["snippets"])
            llm_output = ask_medllama(query.text, base_context, lang_key, force_format=True)
        else:
            base_context = context_data["protocols"].get("English", "")
            llm_output = ask_medllama(query.text, base_context, lang_key)
    
    return {
        "status": "success", "triage_level": context_data["level"], "color": context_data["color"],
        "isEmergency": context_data["isEmerg"], "sysText": context_data["sysText"],
        "visual_path": context_data["visual"], "llm_response": llm_output
    }

from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

@app.get("/api/tts")
def tts_proxy(q: str, tl: str = "en"):
    """Proxy Google TTS to bypass CORS restrictions in the browser."""
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={q}&tl={tl}&client=tw-ob"
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://translate.google.com/"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        return Response(content=r.content, media_type="audio/mpeg")
    except:
        return Response(content=b"", media_type="audio/mpeg", status_code=500)

# Serve the built React frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")
    app.mount("/img", StaticFiles(directory=os.path.join(static_dir, "img")), name="img")
    app.mount("/HUD", StaticFiles(directory=os.path.join(static_dir, "HUD")), name="HUD")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = os.path.join(static_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(static_dir, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

