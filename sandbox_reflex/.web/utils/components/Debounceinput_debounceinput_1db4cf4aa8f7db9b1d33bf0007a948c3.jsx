
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isNotNullOrUndefined,isTrue} from "$/utils/state"
import DebounceInput from "react-debounce-input"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {TextField as RadixThemesTextField} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Debounceinput_debounceinput_1db4cf4aa8f7db9b1d33bf0007a948c3 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_a9bb4b6f12570594a446cd833dd6a356 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_form____form_state.set_f_hotel", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state_form____form_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_form____form_state)



    return(
        jsx(DebounceInput,{css:({ ["width"] : "100%", ["backgroundColor"] : "#262730", ["border"] : "1px solid rgba(250, 250, 250, 0.2)", ["color"] : "white", ["&:focus"] : ({ ["border"] : "1px solid #ff4d4d", ["boxShadow"] : "0 0 0 1px #ff4d4d" }), ["cursor"] : "pointer" }),debounceTimeout:300,disabled:reflex___state____state__sandbox_reflex___state_form____form_state.is_view_only_rx_state_,element:RadixThemesTextField.Root,list:"hoteis_list",onChange:on_change_a9bb4b6f12570594a446cd833dd6a356,placeholder:"Selecione ou busque o hotel...",value:(isNotNullOrUndefined(reflex___state____state__sandbox_reflex___state_form____form_state.f_hotel_rx_state_) ? reflex___state____state__sandbox_reflex___state_form____form_state.f_hotel_rx_state_ : "")},)
    )
});
