
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isNotNullOrUndefined,isTrue} from "$/utils/state"
import DebounceInput from "react-debounce-input"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {TextField as RadixThemesTextField} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Debounceinput_debounceinput_368af7cd2001814285ea011daae45e90 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_0788cda4a7979a2d91428f8fc38efec2 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_hoteis____hotel_state.set_h_nome", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state_hoteis____hotel_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_hoteis____hotel_state)



    return(
        jsx(DebounceInput,{css:({ ["width"] : "100%" }),debounceTimeout:300,element:RadixThemesTextField.Root,onChange:on_change_0788cda4a7979a2d91428f8fc38efec2,placeholder:"Nome...",value:(isNotNullOrUndefined(reflex___state____state__sandbox_reflex___state_hoteis____hotel_state.h_nome_rx_state_) ? reflex___state____state__sandbox_reflex___state_hoteis____hotel_state.h_nome_rx_state_ : "")},)
    )
});
