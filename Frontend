"use client";
import { useState } from "react";
import { motion } from "framer-motion"; // Animation အတွက် (npm install framer-motion)

export default function Home() {
  const [apiKey, setApiKey] = useState("");
  const [model, setModel] = useState("gemini-1.5-flash");
  const [lang, setLang] = useState("Burmese");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTranslate = async () => {
    if (!file || !apiKey) return alert("Fill all fields!");
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("api_key", apiKey);
    formData.append("model_choice", model);
    formData.append("target_lang", lang);

    try {
      const res = await fetch("http://localhost:8000/translate", { method: "POST", body: formData });
      const data = await res.json();
      
      const element = document.createElement("a");
      element.href = URL.createObjectURL(new Blob([data.translated_srt], {type: 'text/plain'}));
      element.download = `translated_${lang}.srt`;
      element.click();
      
      alert("Success!");
    } catch (err) {
      alert("Error occurred!");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white flex items-center justify-center p-6">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gray-800 p-8 rounded-3xl shadow-2xl w-full max-w-xl border border-gray-700"
      >
        <h1 className="text-3xl font-extrabold text-center mb-6 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
          AI Subtitle Pro
        </h1>

        <div className="space-y-4">
          <input type="password" placeholder="Gemini API Key" className="w-full p-4 rounded-xl bg-gray-900 border border-gray-600 focus:ring-2 focus:ring-blue-500 outline-none" onChange={(e) => setApiKey(e.target.value)} />
          
          <div className="flex gap-4">
            <select className="flex-1 p-4 rounded-xl bg-gray-900 border border-gray-600" onChange={(e) => setModel(e.target.value)}>
              <option value="gemini-1.5-flash">Gemini Flash</option>
              <option value="gemini-1.5-pro">Gemini Pro</option>
            </select>
            
            <select className="flex-1 p-4 rounded-xl bg-gray-900 border border-gray-600" onChange={(e) => setLang(e.target.value)}>
              <option value="Burmese">Burmese</option>
              <option value="English">English</option>
              <option value="Thai">Thai</option>
              <option value="Korean">Korean</option>
              <option value="Japanese">Japanese</option>
            </select>
          </div>

          <div className="p-6 border-2 border-dashed border-gray-600 rounded-2xl text-center hover:bg-gray-700 transition">
            <input type="file" accept=".srt" onChange={(e) => setFile(e.target.files[0])} className="cursor-pointer" />
          </div>

          <button 
            onClick={handleTranslate} 
            disabled={loading}
            className={`w-full p-4 rounded-2xl font-bold text-lg transition-all ${loading ? 'bg-gray-600' : 'bg-blue-600 hover:bg-blue-500 shadow-lg shadow-blue-900/20'}`}
          >
            {loading ? (
              <div className="flex flex-col items-center">
                <span>Translating...</span>
                <motion.div 
                  className="h-1 bg-blue-400 mt-2 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: "100%" }}
                  transition={{ duration: 10, ease: "linear" }}
                />
              </div>
            ) : "Start Translation"}
          </button>
        </div>
      </motion.div>
    </div>
  );
}
