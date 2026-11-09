import streamlit as st
import openai
import google.generativeai as genai

# Sayt tənzimləmələri
st.set_page_config(page_title="AI Komitəsi", page_icon="🤖", layout="centered")
st.title("🤖 AI Komitəsi (ChatGPT + Gemini + Grok)")
st.write("Sualını yaz; ChatGPT, Gemini və Grok müzakirə etsin, ortaq yekun qərarı sənə təqdim etsinlər.")

# Sol paneldə API açarları üçün xanalar
with st.sidebar:
    st.header("🔑 API Tənzimləmələri")
    openai_key = st.text_input("OpenAI (ChatGPT) API Key", type="password")
    gemini_key = st.text_input("Gemini API Key", type="password")
    grok_key = st.text_input("Grok (xAI) API Key", type="password")
    st.info("Hər üç modeli işə salmaq üçün açarlarını bura daxil et.")

user_prompt = st.text_area("Sualınızı və ya tapşırığınızı daxil edin:", placeholder="Məsələn: Roblox skriptində optimizasiya...")

if st.button("Müzakirəni Başlat və Qərar Ver"):
    if not openai_key or not gemini_key or not grok_key:
        st.error("Zəhmət olmasa sol paneldən **hər üç** API açarını daxil et!")
    elif not user_prompt:
        st.warning("Zəhmət olmasa bir sual yaz!")
    else:
        with st.spinner("Üç nəhəng AI (ChatGPT, Gemini, Grok) düşünür və müzakirə edir..."):
            try:
                # 1. ChatGPT-nin cavabı
                openai.api_key = openai_key
                gpt_response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": user_prompt}]
                )
                gpt_text = gpt_response.choices[0].message.content

                # 2. Gemini-nin cavabı
                genai.configure(api_key=gemini_key)
                gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                gemini_response = gemini_model.generate_content(user_prompt)
                gemini_text = gemini_response.text

                # 3. Grok-un cavabı (xAI API)
                grok_client = openai.OpenAI(
                    api_key=grok_key,
                    base_url="https://api.x.ai/v1"
                )
                grok_response = grok_client.chat.completions.create(
                    model="grok-2-latest",
                    messages=[{"role": "user", "content": user_prompt}]
                )
                grok_text = grok_response.choices[0].message.content

                # 4. Yekun Ortaq Qərar (Master Analiz)
                consensus_prompt = f"""
                Sən baş idarəçi bir AI-san. Aşağıda üç fərqli süni intellekt modelinin (ChatGPT, Gemini və Grok) eyni suala verdiyi cavablar var. 
                Bu cavabları müqayisə et, hər birinin ən güclü tərəflərini birləşdir və ən mükəmməl yekun ortaq cavabı hazırla:
                
                - ChatGPT cavabı: {gpt_text}
                - Gemini cavabı: {gemini_text}
                - Grok cavabı: {grok_text}
                """
                consensus_response = gemini_model.generate_content(consensus_prompt)
                final_text = consensus_response.text

                # Nəticələrin ekranda göstərilməsi
                st.subheader("💡 Ortaq Yekun Qərar (Komitənin Qərarı)")
                st.success(final_text)

                with st.expander("Göstər: Hər 3 modelin fərdi cavabları"):
                    tab1, tab2, tab3 = st.tabs(["🟢 ChatGPT", "🔵 Gemini", "⚡ Grok"])
                    with tab1:
                        st.write(gpt_text)
                    with tab2:
                        st.write(gemini_text)
                    with tab3:
                        st.write(grok_text)

            except Exception as e:
                st.error(f"Xəta baş verdi: {e}")
