
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Select as RadixThemesSelect} from "@radix-ui/themes"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Selectroot_select__root_36859da50d4cb628f9a28275f34bdb5c = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_a40ccf16251944c3e4038bb10144a51c = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state.set_ano_ref", ({ ["ano"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state)



    return(
        jsx(RadixThemesSelect.Root,{css:({ ["cursor"] : "pointer" }),onValueChange:on_change_a40ccf16251944c3e4038bb10144a51c,value:reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.ano_ref_rx_state_},children)
    )
});
