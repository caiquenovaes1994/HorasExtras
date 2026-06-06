
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isNotNullOrUndefined,isTrue} from "$/utils/state"
import DebounceInput from "react-debounce-input"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {TextField as RadixThemesTextField} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Debounceinput_debounceinput_9d6eb9d1ff8093d048c7e597773a06eb = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_0e20a6ed623ed3ea231f2e6c2cf0fc78 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state.set_mes_ref", ({ ["mes"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state)



    return(
        jsx(DebounceInput,{css:({ ["width"] : "200px", ["backgroundColor"] : "#262730", ["border"] : "1px solid rgba(250, 250, 250, 0.2)", ["color"] : "white", ["&:focus"] : ({ ["border"] : "1px solid #ff4d4d", ["boxShadow"] : "0 0 0 1px #ff4d4d" }), ["cursor"] : "pointer" }),debounceTimeout:300,element:RadixThemesTextField.Root,list:"meses_list",onChange:on_change_0e20a6ed623ed3ea231f2e6c2cf0fc78,value:(isNotNullOrUndefined(reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.mes_ref_rx_state_) ? reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.mes_ref_rx_state_ : "")},)
    )
});
