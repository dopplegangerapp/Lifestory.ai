// Interview system functionality
document.addEventListener('DOMContentLoaded', function() {
    const answerForm = document.getElementById('answer-form');
    const answerInput = document.getElementById('answer');
    const questionDisplay = document.getElementById('current-question');
    const stageDisplay = document.getElementById('current-stage');
    const progressBar = document.getElementById('progress-bar');
    const followUpContainer = document.getElementById('follow-up-questions');
    
    let currentStage = 'foundations';
    let currentQuestionIndex = 0;
    
    // Update UI with current question and stage
    function updateUI() {
        const stage = INTERVIEW_STAGES[currentStage];
        questionDisplay.textContent = stage.questions[currentQuestionIndex];
        stageDisplay.textContent = stage.name;
        
        // Update progress bar
        const totalQuestions = Object.values(INTERVIEW_STAGES)
            .reduce((sum, stage) => sum + stage.questions.length, 0);
        const currentProgress = Object.keys(INTERVIEW_STAGES)
            .indexOf(currentStage) * 100 / Object.keys(INTERVIEW_STAGES).length;
        progressBar.style.width = `${currentProgress}%`;
    }
    
    // Display follow-up questions
    function displayFollowUpQuestions(questions) {
        if (!questions || questions.length === 0) return;
        
        followUpContainer.innerHTML = '<h3>Follow-up Questions</h3>';
        const list = document.createElement('ul');
        questions.forEach(question => {
            const item = document.createElement('li');
            item.textContent = question;
            list.appendChild(item);
        });
        followUpContainer.appendChild(list);
        followUpContainer.style.display = 'block';
    }
    
    // Handle form submission
    answerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const answer = answerInput.value.trim();
        if (!answer) return;
        
        try {
            const response = await fetch('/api/interview/answer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    answer: answer
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Move to next question or stage
                const stage = INTERVIEW_STAGES[currentStage];
                if (currentQuestionIndex < stage.questions.length - 1) {
                    currentQuestionIndex++;
                } else if (stage.next) {
                    currentStage = stage.next;
                    currentQuestionIndex = 0;
                } else {
                    // Interview complete
                    window.location.href = '/cards';
                }
                
                updateUI();
                answerInput.value = '';
                // Clear any error message
                const errorDisplay = document.getElementById('error-message');
                if (errorDisplay) {
                    errorDisplay.remove();
                }
                
                // Display follow-up questions if any
                if (data.follow_up_questions) {
                    displayFollowUpQuestions(data.follow_up_questions);
                }
            } else {
                // Display error message
                const errorDisplay = document.createElement('div');
                errorDisplay.id = 'error-message';
                errorDisplay.className = 'error-message';
                errorDisplay.textContent = data.error;
                answerForm.insertBefore(errorDisplay, answerInput);
            }
        } catch (error) {
            console.error('Error submitting answer:', error);
        }
    });
    
    // Initial UI update
    updateUI();
}); 