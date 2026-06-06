
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isNotNullOrUndefined,isTrue} from "$/utils/state"
import DebounceInput from "react-debounce-input"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {TextField as RadixThemesTextField} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Debounceinput_debounceinput_e79b3b1a2b441b4e5730b8af9d726730 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_2b50bf15f186fb137fcab962ed510d9c = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_hoteis____hotel_state.set_h_rid", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state_hoteis____hotel_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_hoteis____hotel_state)



    return(
        jsx(DebounceInput,{css:({ ["width"] : "100%" }),debounceTimeout:300,disabled:!((reflex___state____state__sandbox_reflex___state_hoteis____hotel_state.h_original_rid_rx_state_?.valueOf?.() === ""?.valueOf?.())),element:RadixThemesTextField.Root,onChange:on_change_2b50bf15f186fb137fcab962ed510d9c,placeholder:"Ex: ABCDE",value:(isNotNullOrUndefined(reflex___state____state__sandbox_reflex___state_hoteis____hotel_state.h_rid_rx_state_) ? reflex___state____state__sandbox_reflex___state_hoteis____hotel_state.h_rid_rx_state_ : "")},)
    )
});
