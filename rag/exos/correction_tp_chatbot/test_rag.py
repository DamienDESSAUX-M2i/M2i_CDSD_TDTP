from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset
import time

def evaluate_rag_system(rag_pipeline, test_dataset):
    """
    Evalue le systeme RAG complet avec RAGAS.
    """
    print("Debut de l'evaluation...\n")
    
    # Collecter les resultats
    results = []
    
    for item in test_dataset:
        question = item['question']
        print(f"Question {item['id']}: {question}")
        
        try:
            # Obtenir la reponse du RAG
            start_time = time.time()
            response = rag_pipeline.answer(question)
            elapsed_time = time.time() - start_time
            
            # Formater pour RAGAS
            result = {
                "question": question,
                "answer": response['answer'],
                "contexts": response['contexts'],
                "ground_truth": item['expected_answer'],
                "response_time": elapsed_time,
                "sources": response['sources'],
                "category": item['category'],
                "difficulty": item['difficulty']
            }
            
            results.append(result)
            print(f"Reponse generee en {elapsed_time:.2f}s\n")
            
        except Exception as e:
            print(f"Erreur: {e}\n")
            continue
    
    # Convertir en Dataset pour RAGAS
    ragas_dataset = Dataset.from_dict({
        "question": [r['question'] for r in results],
        "answer": [r['answer'] for r in results],
        "contexts": [r['contexts'] for r in results],
        "ground_truth": [r['ground_truth'] for r in results]
    })
    
    # Evaluation RAGAS
    print("\nEvaluation avec RAGAS...")
    ragas_results = evaluate(
        ragas_dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall
        ]
    )
    
    # Ajouter les scores RAGAS aux resultats
    for i, result in enumerate(results):
        result['ragas_scores'] = {
            'faithfulness': ragas_results['faithfulness'][i] if i < len(ragas_results['faithfulness']) else None,
            'answer_relevancy': ragas_results['answer_relevancy'][i] if i < len(ragas_results['answer_relevancy']) else None,
            'context_precision': ragas_results['context_precision'][i] if i < len(ragas_results['context_precision']) else None,
            'context_recall': ragas_results['context_recall'][i] if i < len(ragas_results['context_recall']) else None,
        }
    
    return results, ragas_results
