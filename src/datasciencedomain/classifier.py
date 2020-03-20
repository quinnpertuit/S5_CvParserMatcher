import math
from functools import partial
from multiprocessing.pool import Pool

# from datasciencedomain import misc
from datasciencedomain.semanticmodule import Semantic as sema
from datasciencedomain.syntacticmodule import Syntactic as synt
from datasciencedomain.ontology import Ontology as CSO
from datasciencedomain.model import Model as MODEL
from datasciencedomain.paper import Paper
from datasciencedomain.result import Result
# from classifier.config import Config

def run_domain_classifier(paper, modules="both", enhancement="first", explanation=False):

    if modules not in ["syntactic", "semantic", "both"]:
        raise ValueError("Error: Field modules must be 'syntactic', 'semantic' or 'both'")

    if enhancement not in ["first", "all", "no"]:
        raise ValueError("Error: Field enhances must be 'first', 'all' or 'no'")
    
    if type(explanation) != bool:
        raise ValueError("Error: Explanation must be set to either True or False")

    
    # Loading ontology and model
    cso = CSO()
    model = MODEL()
    t_paper = Paper(paper, modules)
    result = Result(explanation)

    # Passing parameters to the two classes (synt and sema) and actioning classifiers

    if modules == 'syntactic' or modules == 'both':
        synt_module = synt(cso, t_paper)
        result.set_syntactic(synt_module.classify_syntactic())
        if explanation: result.dump_temporary_explanation(synt_module.get_explanation())
    if modules == 'semantic' or modules == 'both':
        sema_module = sema(model, cso, t_paper)
        result.set_semantic(sema_module.classify_semantic())
        if explanation: result.dump_temporary_explanation(sema_module.get_explanation())
       
    result.set_enhanced(cso.climb_ontology(getattr(result, "union"), enhancement))


    return result.get_dict()
