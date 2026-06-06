
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Select as RadixThemesSelect} from "@radix-ui/themes"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Selectroot_select__root_56e9f3412f1983dbe5c40c23c7ea94b1 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_78b63321551380a4883ac9ec4ce6eb72 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state.set_mes_ref", ({ ["mes"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state)



    return(
        jsx(RadixThemesSelect.Root,{css:({ ["cursor"] : "pointer" }),onValueChange:on_change_78b63321551380a4883ac9ec4ce6eb72,value:reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.mes_ref_rx_state_},children)
    )
});
