
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isNotNullOrUndefined,isTrue} from "$/utils/state"
import DebounceInput from "react-debounce-input"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {TextField as RadixThemesTextField} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Debounceinput_debounceinput_53e54501f0fa3202272b4e0490dc95cc = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_2f0e3a48333773dc4848353ff8049e3f = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.set_p_valor_base", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state____auth_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state)



    return(
        jsx(DebounceInput,{css:({ ["width"] : "100%" }),debounceTimeout:300,element:RadixThemesTextField.Root,onChange:on_change_2f0e3a48333773dc4848353ff8049e3f,placeholder:"Ex: 15.50",value:(isNotNullOrUndefined(reflex___state____state__sandbox_reflex___state____auth_state.p_valor_base_rx_state_) ? reflex___state____state__sandbox_reflex___state____auth_state.p_valor_base_rx_state_ : "")},)
    )
});
