from classifier import run_cso_classifier

paper2  = {
        "abstract": "Apply clustering in order gaussian naive bayes to group data obtained from ECG signals and find heartbeat candidates. Internal software (Core Banking System) conception and development from the database to the interface. BPA & RPA (Business and Robotic Process Automation) for different projects includingits visualization and data analysis. Automate management tools including visualization and data analysis for which I developed a follow up software. Interface coordination between commercial and development teams, deliverables. Developed a follow up software, follow up projects. Data analysis and visualization. Management reports. Developed a follow up software, follow up projects. Data analysis and visualization. Management reports. Artificial Intelligence {ML, DL, NLP}, Languages and Logic, Graphs, Software Engineering, Mathematics {Proba, Stat, Alg}, Signal Processing, Operational Research, Big Data, Data Mining, B.I. ◦ (S5) Parser and matcher of a recruitment oer ◦ (S4) Ship detection by using satellite images, AI + Statistics ◦ Expr - Pfx Compiler (lambda, sematics, languages) ◦ Social Networks treatment (graphs) and infection simulation ◦ Genetic algorithm for heating district network optimization (OR) ◦ Cloud Configuration + tf-idf on Big Data",
        "keywords": "data mining, computer science"
        }


result = run_cso_classifier(paper2, modules = "both", enhancement = "first", explanation = True)
print(result)