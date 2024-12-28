const prompt = 'Can you please respond with saying "Hello", who you are and which version you are?'

// // GEMINI API
const GEMINI_KEY = 'AIzaSyBzq5-pVkLM-Mv8CVn0X1sCpgg75PDXpoI';
const { GoogleGenerativeAI } = require('@google/generative-ai');

const genAI = new GoogleGenerativeAI(GEMINI_KEY);
const model = genAI.getGenerativeModel({model: 'gemini-1.5-flash'});

runGemini();

async function runGemini() {

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    console.log(response);
    console.log(text);
}


// // OPENAI API
// const OPENAI_KEY = 'sk-uPNj9GtVtIJyDMXSfXgMK2jYUB3Gmvt1GMQVfWHSmMT3BlbkFJCfCbCd2Yl5sCYEVMuLJxJ5Fv3SkvAIyE-bRbhv1WwA';
// const { OpenAI } = require('openai');

// const openAI = new OpenAI({apiKey: OPENAI_KEY});

// runChatGPT();

// async function runChatGPT() {

//     const response = await openAI.chat.completions.create({
//         messages: [
//             {
//                 role:'user',
//                 content: prompt
//             }
//         ],
//         model: 'gpt-4o-mini'
//     });
//     const text = response.choices[0].message;
//     console.log(text);
// }