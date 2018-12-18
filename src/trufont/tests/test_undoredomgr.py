"""  Class and  """
import sys
import logging
import os

from typing import Optional, Any, Union, Tuple

import trufont.util.deco4class as deco4class
import trufont.util.loggingstuff as logstuff

import trufont.objects.undoredomgr as undoredomgr
# constants


def test_undoredomgr(logger: logging.Logger = logging.getLogger(logstuff.LOGGER_UNDOREDO)):
    """ Untis Tests for UndoRedoMgr"""

    logger.setLevel(logging.DEBUG)
    logger.info("======== Start of test")
    logger.info(sys.version)
    mgr = undoredomgr.UndoRedoMgr("test", logger)
    mgr.set_callback_after_undo(print, "\t"*3, "callback on undo")
    mgr.set_callback_after_redo(print, "\t"*4, "CALLBACK ON REDO")
    mgr.set_callback_error_undoredo(logging.error, "Error on Undo or Redo - Stacks are empty now")

    seq = 1
    assert (mgr.can_redo() == False and mgr.can_undo() == False) 
    logger.info("{:02d} -> undo: {} / redo: {}".format(seq, mgr.all_actions_undo(), mgr.all_actions_redo()))

    try: 
        mgr.undo()
    except Exception as e:
        logger.warning("{:02d} -> Except - undo on an empty stack".format(seq))
        assert isinstance(e, IndexError) and mgr.len_undo() == 0

    seq += 1
    try:
        with mgr.undo_ctx() as action:
            logger.warning("{:02d} -> Except - undo on an empty stack".format(seq))
            # assert False
    except Exception as e:    
        assert isinstance(e, RuntimeError) and mgr.len_undo() == 0
    logger.info("{:02d} -> undo: {} / redo: {}".format(seq, mgr.all_actions_undo(), mgr.all_actions_redo()))

    seq += 1
    mgr.append_action(undoredomgr.Action("A", None, None))
    with mgr.undo_ctx() as action:
        1/0
    assert (mgr.len_undo() == mgr.len_redo() == 0)
    logger.info("{:02d} -> undo: {} / redo: {}".format(seq, mgr.all_actions_undo(), mgr.all_actions_redo()))

 
    seq += 1
    logger.info(mgr.str_state())
    mgr.append_action(undoredomgr.Action("A", None, None))
    mgr.append_action(undoredomgr.Action("B", logger.info("test callback undo"), None))
    assert mgr.len_undo() == 2 and mgr.len_redo() == 0
    logger.info("{:02d} -> undo: {} / redo: {}".format(seq, mgr.all_actions_undo(), mgr.all_actions_redo()))

    seq += 1
    action = mgr.undo()
    assert mgr.len_undo() == 1 and mgr.len_redo() == 1
    logger.info("{:02d} -> undo: {} / redo: {}".format(seq, mgr.all_actions_undo(), mgr.all_actions_redo()))

    seq += 1
    action = mgr.redo()
    assert mgr.len_undo() == 2 and mgr.len_redo() == 0
    logger.info("{:02d} -> undo: {} / redo: {}".format(seq, mgr.all_actions_undo(), mgr.all_actions_redo()))
    
    seq += 1
    action = mgr.undo()
    assert mgr.len_undo() == 1 and mgr.len_redo() == 1
    logger.info("{:02d} -> undo: {} / redo: {}".format(seq, mgr.all_actions_undo(), mgr.all_actions_redo()))

    seq += 1
    mgr.append_action(action)
    mgr.append_action(undoredomgr.Action('C', None, None))
    assert mgr.len_undo() == 3 and mgr.len_redo() == 0
    logger.info("{:02d} -> undo: {} / redo: {}".format(seq, mgr.all_actions_undo(), mgr.all_actions_redo()))

    seq += 1
    action = mgr.undo()
    assert mgr.len_undo() == 2 and mgr.len_redo() == 1
    logger.error("{:02d} -> undo: {} / redo: {}".format(seq, mgr.all_actions_undo(), mgr.all_actions_redo()))
    
    seq += 1
    action = mgr.redo()
    assert mgr.len_undo() == 3 and mgr.len_redo() == 0
    logger.info("{:02d} -> undo: {} / redo: {}".format(seq, mgr.all_actions_undo(), mgr.all_actions_redo()))

    seq += 1
    try:
        action = mgr.redo()
    except Exception as e:
        logger.warning("Except - redo on an empty stack")
        assert isinstance(e, IndexError) and mgr.len_redo() == 0
    logger.info("{:02d} -> undo: {} / redo: {}".format(seq, mgr.all_actions_undo(), mgr.all_actions_redo()))

    seq += 1
    len_undo = mgr.len_undo()
    for _ in range(len_undo):
        action = mgr.undo()
    assert mgr.len_undo() == 0 and mgr.len_redo() == 3
    logger.info("{:02d} -> undo: {} / redo: {}".format(seq, mgr.all_actions_undo(), mgr.all_actions_redo()))
    
    logger.info("----------- End of test")
    

if __name__ == "__main__":
	test_undoredomgr()