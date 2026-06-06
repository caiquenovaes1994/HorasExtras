
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isNotNullOrUndefined,isTrue} from "$/utils/state"
import DebounceInput from "react-debounce-input"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {TextField as RadixThemesTextField} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Debounceinput_debounceinput_745bd75928578c671e952c57f50d9881 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_e10140dc7c3f755457ac1f18653da309 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.set_p_new_password", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state____auth_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state)



    return(
        jsx(DebounceInput,{css:({ ["width"] : "100%" }),debounceTimeout:300,element:RadixThemesTextField.Root,onChange:on_change_e10140dc7c3f755457ac1f18653da309,placeholder:"Digite a nova senha...",type:"password",value:(isNotNullOrUndefined(reflex___state____state__sandbox_reflex___state____auth_state.p_new_password_rx_state_) ? reflex___state____state__sandbox_reflex___state____auth_state.p_new_password_rx_state_ : "")},)
    )
});
