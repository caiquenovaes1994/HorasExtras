
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isNotNullOrUndefined,isTrue} from "$/utils/state"
import DebounceInput from "react-debounce-input"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {TextField as RadixThemesTextField} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Debounceinput_debounceinput_17c5a5d2d9346a5b9ae4724d730649a2 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_8dba803a86542b461404de688a3ffc51 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.set_p_nome", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state____auth_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state)



    return(
        jsx(DebounceInput,{css:({ ["width"] : "100%" }),debounceTimeout:300,element:RadixThemesTextField.Root,onChange:on_change_8dba803a86542b461404de688a3ffc51,placeholder:"Seu nome...",value:(isNotNullOrUndefined(reflex___state____state__sandbox_reflex___state____auth_state.p_nome_rx_state_) ? reflex___state____state__sandbox_reflex___state____auth_state.p_nome_rx_state_ : "")},)
    )
});
