
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isNotNullOrUndefined,isTrue} from "$/utils/state"
import DebounceInput from "react-debounce-input"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {TextField as RadixThemesTextField} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Debounceinput_debounceinput_057f978898710380c483e77bda215081 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_3c592d68fccf6d3d6232fa44520a0dac = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_usuarios____usuario_state.set_u_username", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state_usuarios____usuario_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_usuarios____usuario_state)



    return(
        jsx(DebounceInput,{css:({ ["width"] : "100%" }),debounceTimeout:300,element:RadixThemesTextField.Root,onChange:on_change_3c592d68fccf6d3d6232fa44520a0dac,placeholder:"johndoe",value:(isNotNullOrUndefined(reflex___state____state__sandbox_reflex___state_usuarios____usuario_state.u_username_rx_state_) ? reflex___state____state__sandbox_reflex___state_usuarios____usuario_state.u_username_rx_state_ : "")},)
    )
});
