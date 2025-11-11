// 3-Question Quiz to Route Users

const quizQuestions = [
    {
        id: 1,
        question: "What's your biggest challenge right now?",
        options: [
            { text: "We don't understand what customers actually want", path: "market", weight: 3 },
            { text: "Competitors are winning and we don't know why", path: "competitors", weight: 3 },
            { text: "We're unsure where the market is heading", path: "prediction", weight: 3 }
        ]
    },
    {
        id: 2,
        question: "What timeline are you working with?",
        options: [
            { text: "Need insights within 1-2 weeks (urgent decision)", path: "market", weight: 2 },
            { text: "Planning 1-3 months ahead", path: "competitors", weight: 2 },
            { text: "Strategic planning 6-12 months out", path: "prediction", weight: 2 }
        ]
    },
    {
        id: 3,
        question: "What kind of data interests you most?",
        options: [
            { text: "Customer complaints and feature requests", path: "market", weight: 1 },
            { text: "Competitor weaknesses and gaps", path: "competitors", weight: 1 },
            { text: "Early trend signals and forecasts", path: "prediction", weight: 1 }
        ]
    }
];

let quizState = {
    currentQuestion: 0,
    scores: { market: 0, competitors: 0, prediction: 0 }
};

function startQuiz() {
    // Hide paths, show quiz
    document.getElementById('paths').classList.add('hidden');
    document.getElementById('quiz').classList.remove('hidden');
    
    // Reset state
    quizState = {
        currentQuestion: 0,
        scores: { market: 0, competitors: 0, prediction: 0 }
    };
    
    renderQuestion();
}

function renderQuestion() {
    const question = quizQuestions[quizState.currentQuestion];
    const container = document.getElementById('quiz-container');
    
    container.innerHTML = `
        <div class="quiz-card">
            <div class="quiz-progress">
                Question ${quizState.currentQuestion + 1} of ${quizQuestions.length}
            </div>
            
            <h2 class="quiz-question">${question.question}</h2>
            
            <div class="quiz-options">
                ${question.options.map((option, index) => `
                    <button class="quiz-option" onclick="selectOption(${index})">
                        ${option.text}
                    </button>
                `).join('')}
            </div>
            
            ${quizState.currentQuestion > 0 ? `
                <button class="btn btn-secondary quiz-back" onclick="previousQuestion()">
                    ← Back
                </button>
            ` : ''}
        </div>
    `;
}

function selectOption(optionIndex) {
    const question = quizQuestions[quizState.currentQuestion];
    const selectedOption = question.options[optionIndex];
    
    // Add score
    quizState.scores[selectedOption.path] += selectedOption.weight;
    
    // Next question or show result
    if (quizState.currentQuestion < quizQuestions.length - 1) {
        quizState.currentQuestion++;
        renderQuestion();
    } else {
        showQuizResult();
    }
}

function previousQuestion() {
    if (quizState.currentQuestion > 0) {
        quizState.currentQuestion--;
        renderQuestion();
    }
}

function showQuizResult() {
    // Calculate winning path
    const winner = Object.keys(quizState.scores).reduce((a, b) => 
        quizState.scores[a] > quizState.scores[b] ? a : b
    );
    
    const pathNames = {
        market: "Market Understanding",
        competitors: "Competitive Intelligence",
        prediction: "Trend Prediction"
    };
    
    const container = document.getElementById('quiz-container');
    container.innerHTML = `
        <div class="quiz-result">
            <h2>Based on your answers...</h2>
            <h3 class="result-path">${pathNames[winner]}</h3>
            <p>is the best starting point for your challenge.</p>
            <button class="btn btn-primary" onclick="selectPath('${winner}')">
                Show me this path →
            </button>
            <button class="btn btn-secondary" onclick="resetQuiz()">
                Restart quiz
            </button>
        </div>
    `;
}

function resetQuiz() {
    document.getElementById('quiz').classList.add('hidden');
    document.getElementById('paths').classList.remove('hidden');
}