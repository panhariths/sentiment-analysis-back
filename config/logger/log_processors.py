import datetime
import inspect

from structlog._frames import _find_first_app_frame_and_name


def time_stamp_processor(logger, _, event_dict):
    event_dict["time"] = datetime.datetime.now().isoformat()
    return event_dict


def service_name_processor(logger, _, event_dict):
    event_dict["service"] = "resource"
    return event_dict


def module_info_processor(logger, _, event_dict):
    frame, name = _find_first_app_frame_and_name(
        additional_ignores=["logging", "uvicorn", "asyncio", "click", __name__]
    )
    if not frame:
        return event_dict
    frameinfo = inspect.getframeinfo(frame)
    if not frameinfo:
        return event_dict
    module = inspect.getmodule(frame)
    if not module:
        return event_dict

    event_dict["caller"] = "{}.{}.{}".format(
        module.__name__,
        frameinfo.function,
        frameinfo.lineno,
    )
    return event_dict
