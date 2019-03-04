%run oner.py -l ./lenses_fromLecture.tab ./result_model.txt --condition confidence|error_rate
%run oner.py -c ./result_model.txt lenses.tab result_of_classification.tab
%run compare_results_of_classif.py