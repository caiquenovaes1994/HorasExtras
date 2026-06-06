
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isNotNullOrUndefined,isTrue} from "$/utils/state"
import DebounceInput from "react-debounce-input"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {TextField as RadixThemesTextField} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Debounceinput_debounceinput_8f518e04ba30ac62706e590eebbdee5c = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_187541d29aa5b7bebd0672b19113604c = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_form____form_state.set_f_caso", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state_form____form_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_form____form_state)



    return(
        jsx(DebounceInput,{css:({ ["width"] : "100%" }),debounceTimeout:300,disabled:reflex___state____state__sandbox_reflex___state_form____form_state.is_view_only_rx_state_,element:RadixThemesTextField.Root,onChange:on_change_187541d29aa5b7bebd0672b19113604c,placeholder:"Caso...",value:(isNotNullOrUndefined(reflex___state____state__sandbox_reflex___state_form____form_state.f_caso_rx_state_) ? reflex___state____state__sandbox_reflex___state_form____form_state.f_caso_rx_state_ : "")},)
    )
});
