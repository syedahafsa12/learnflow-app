import React, { useState } from 'react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import ProgressBar from '../components/ui/ProgressBar';
import Badge from '../components/ui/Badge';
import { useUser } from '../context/UserContext';

const QuizView = () => {
  const { user } = useUser();
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [quizCompleted, setQuizCompleted] = useState(false);
  const [score, setScore] = useState(0);

  const questions = [
    {
      id: 1,
      question: "What is the correct syntax for a for loop in Python?",
      options: [
        "for i in range(5):",
        "loop i from 1 to 5:",
        "repeat 5 times:",
        "for (i=0; i<5; i++)"
      ],
      correct: 0
    },
    {
      id: 2,
      question: "Which statement is used to exit a loop in Python?",
      options: ["break", "stop", "exit", "return"],
      correct: 0
    },
    {
      id: 3,
      question: "What does the 'continue' statement do in a loop?",
      options: [
        "Ends the loop completely",
        "Skips the rest of the current iteration",
        "Pauses the loop",
        "Restarts the loop"
      ],
      correct: 1
    }
  ];

  const handleAnswerSelect = (questionId, answerIndex) => {
    setSelectedAnswers({ ...selectedAnswers, [questionId]: answerIndex });
  };

  const handleSubmitQuiz = () => {
    let correctCount = 0;
    questions.forEach(q => { if (selectedAnswers[q.id] === q.correct) correctCount++; });
    setScore(Math.round((correctCount / questions.length) * 100));
    setQuizCompleted(true);
  };

  if (quizCompleted) {
    return (
      <div className="max-w-2xl mx-auto space-y-8 py-10 animate-in zoom-in duration-500">
        <Card className="!p-12 text-center relative overflow-hidden">
          <div className={`absolute top-0 inset-x-0 h-2 ${score >= 70 ? 'bg-emerald-500' : 'bg-amber-500'}`}></div>
          <div className="w-32 h-32 rounded-[2.5rem] bg-slate-900 text-white flex flex-col items-center justify-center mx-auto mb-8 shadow-2xl">
            <span className="text-4xl font-black">{score}%</span>
          </div>
          <h2 className="text-3xl font-black text-slate-900 mb-4">Assessment Complete!</h2>
          <p className="text-slate-500 font-medium leading-relaxed mb-8 max-w-sm mx-auto">
            {score >= 70 
              ? "Exceptional! You've demonstrated high proficiency in Control Flow concepts." 
              : "Valid effort! A quick review of Loop syntax will help push you to the next level."}
          </p>
          <div className="flex gap-4 max-w-sm mx-auto">
             <Button variant="primary" className="flex-1" onClick={() => setQuizCompleted(false) || setSelectedAnswers({}) || setCurrentQuestion(0)}>Retake</Button>
             <Button variant="outline" className="flex-1">Review</Button>
          </div>
        </Card>

        <Card title="Question Analytics">
           <div className="space-y-6">
              {questions.map((q, idx) => (
                <div key={q.id} className="p-6 rounded-[2rem] bg-slate-50 border border-slate-100 flex flex-col gap-4">
                  <div className="flex justify-between items-start">
                    <p className="text-sm font-black text-slate-900 max-w-[80%]">Q{idx + 1}: {q.question}</p>
                    <Badge variant={selectedAnswers[q.id] === q.correct ? 'success' : 'danger'}>
                       {selectedAnswers[q.id] === q.correct ? 'Correct' : 'Incorrect'}
                    </Badge>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 border-t border-slate-200/50">
                     <div className="space-y-1">
                        <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Your Choice</p>
                        <p className={`text-xs font-bold ${selectedAnswers[q.id] === q.correct ? 'text-emerald-600' : 'text-rose-600'}`}>
                          {q.options[selectedAnswers[q.id]] || 'No Selection'}
                        </p>
                     </div>
                     <div className="space-y-1">
                        <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Correct Solution</p>
                        <p className="text-xs font-bold text-slate-900">{q.options[q.correct]}</p>
                     </div>
                  </div>
                </div>
              ))}
           </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto space-y-8 pb-12 animate-in fade-in duration-700">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div className="space-y-2">
          <div className="inline-flex items-center space-x-2 px-3 py-1 bg-amber-50 text-amber-700 rounded-full text-[10px] font-black uppercase tracking-widest ring-1 ring-amber-200">
             Active Assessment
          </div>
          <h1 className="text-4xl font-black tracking-tight text-slate-900">Quiz Master</h1>
          <p className="text-slate-500 font-medium">Topic: Python Control Flow</p>
        </div>
        <div className="text-right">
           <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Module Progress</p>
           <p className="text-sm font-black text-slate-900">{currentQuestion + 1} of {questions.length}</p>
        </div>
      </div>

      <ProgressBar value={currentQuestion + 1} max={questions.length} variant="premium" className="!h-1.5" />

      <Card className="!p-12">
        <div className="space-y-10">
          <h3 className="text-2xl font-black text-slate-900 leading-tight">
            {questions[currentQuestion]?.question}
          </h3>
          
          <div className="space-y-4">
            {questions[currentQuestion]?.options.map((option, index) => (
              <button
                key={index}
                onClick={() => handleAnswerSelect(questions[currentQuestion].id, index)}
                className={`
                  w-full group flex items-center p-6 rounded-[2rem] border-2 transition-all duration-300
                  ${selectedAnswers[questions[currentQuestion].id] === index
                    ? 'border-indigo-500 bg-indigo-50/50 shadow-lg shadow-indigo-500/5'
                    : 'border-slate-100 hover:border-slate-300 hover:bg-slate-50'}
                `}
              >
                <div className={`
                  w-8 h-8 rounded-xl border-2 flex items-center justify-center mr-6 transition-all font-black text-sm
                  ${selectedAnswers[questions[currentQuestion].id] === index
                    ? 'border-indigo-600 bg-indigo-600 text-white'
                    : 'border-slate-200 text-slate-400 group-hover:border-slate-400'}
                `}>
                  {String.fromCharCode(65 + index)}
                </div>
                <span className={`text-sm font-bold transition-all ${selectedAnswers[questions[currentQuestion].id] === index ? 'text-indigo-900' : 'text-slate-600'}`}>
                   {option}
                </span>
              </button>
            ))}
          </div>

          <div className="flex justify-between items-center pt-6 border-t border-slate-100">
            <Button
              onClick={() => setCurrentQuestion(q => Math.max(0, q - 1))}
              variant="outline"
              disabled={currentQuestion === 0}
            >
              Previous
            </Button>
            
            {currentQuestion < questions.length - 1 ? (
              <Button
                onClick={() => setCurrentQuestion(q => q + 1)}
                disabled={selectedAnswers[questions[currentQuestion].id] === undefined}
                className="px-10"
              >
                Next Step
              </Button>
            ) : (
              <button
                onClick={handleSubmitQuiz}
                disabled={Object.keys(selectedAnswers).length < questions.length}
                className="btn-premium px-12"
              >
                Submit Results
              </button>
            )}
          </div>
        </div>
      </Card>
    </div>
  );
};

export default QuizView;