
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Dialog as RadixThemesDialog} from "@radix-ui/themes"
import {EventLoopContext} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Dialogcontent_dialog__content_fa200ae9bfe4b0b185925ce058b786a3 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_pointer_down_outside_d2f4a32c7dd660fbd7edf67ef06c5ec7 = useCallback(((...args) => (addEvents([(ReflexEvent("_call_function", ({ ["function"] : (() => null), ["callback"] : null }), ({ ["preventDefault"] : true })))], args, ({  })))), [addEvents, ReflexEvent])
const on_escape_key_down_d2f4a32c7dd660fbd7edf67ef06c5ec7 = useCallback(((...args) => (addEvents([(ReflexEvent("_call_function", ({ ["function"] : (() => null), ["callback"] : null }), ({ ["preventDefault"] : true })))], args, ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesDialog.Content,{onEscapeKeyDown:on_escape_key_down_d2f4a32c7dd660fbd7edf67ef06c5ec7,onPointerDownOutside:on_pointer_down_outside_d2f4a32c7dd660fbd7edf67ef06c5ec7},children)
    )
});
