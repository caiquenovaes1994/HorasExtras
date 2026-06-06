
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isNotNullOrUndefined,isTrue} from "$/utils/state"
import DebounceInput from "react-debounce-input"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {TextField as RadixThemesTextField} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Debounceinput_debounceinput_9e69d68830549384a00bfdb0831b8ec9 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_7c00654f550d71d2a9b849ed173f9e5c = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_hoteis____hotel_state.set_search_query", ({ ["query"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state_hoteis____hotel_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_hoteis____hotel_state)



    return(
        jsx(DebounceInput,{css:({ ["width"] : "300px", ["backgroundColor"] : "#262730", ["border"] : "1px solid rgba(250, 250, 250, 0.2)", ["color"] : "white", ["&:focus"] : ({ ["border"] : "1px solid #ff4d4d", ["boxShadow"] : "0 0 0 1px #ff4d4d" }) }),debounceTimeout:300,element:RadixThemesTextField.Root,onChange:on_change_7c00654f550d71d2a9b849ed173f9e5c,placeholder:"\ud83d\udd0d Buscar por RID ou Nome...",value:(isNotNullOrUndefined(reflex___state____state__sandbox_reflex___state_hoteis____hotel_state.search_query_rx_state_) ? reflex___state____state__sandbox_reflex___state_hoteis____hotel_state.search_query_rx_state_ : "")},)
    )
});
