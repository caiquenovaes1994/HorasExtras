
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isNotNullOrUndefined,isTrue} from "$/utils/state"
import DebounceInput from "react-debounce-input"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {TextField as RadixThemesTextField} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Debounceinput_debounceinput_c8b1096bf8ac78b1861cf697934a5304 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_86aeee46496cc2af9d889757d41ad839 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state.set_ano_ref", ({ ["ano"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state)



    return(
        jsx(DebounceInput,{css:({ ["width"] : "120px", ["backgroundColor"] : "#262730", ["border"] : "1px solid rgba(250, 250, 250, 0.2)", ["color"] : "white", ["&:focus"] : ({ ["border"] : "1px solid #ff4d4d", ["boxShadow"] : "0 0 0 1px #ff4d4d" }), ["cursor"] : "pointer" }),debounceTimeout:300,element:RadixThemesTextField.Root,list:"anos_list",onChange:on_change_86aeee46496cc2af9d889757d41ad839,value:(isNotNullOrUndefined(reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.ano_ref_rx_state_) ? reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.ano_ref_rx_state_ : "")},)
    )
});
