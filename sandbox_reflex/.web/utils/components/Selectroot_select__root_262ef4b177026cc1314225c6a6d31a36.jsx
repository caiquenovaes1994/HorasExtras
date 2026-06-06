
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Select as RadixThemesSelect} from "@radix-ui/themes"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Selectroot_select__root_262ef4b177026cc1314225c6a6d31a36 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_change_43061dce0b055d84dcb505bb8e5e3fdd = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_form____form_state.set_f_hotel", ({ ["val"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state_form____form_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_form____form_state)



    return(
        jsx(RadixThemesSelect.Root,{disabled:reflex___state____state__sandbox_reflex___state_form____form_state.is_view_only_rx_state_,onValueChange:on_change_43061dce0b055d84dcb505bb8e5e3fdd,value:reflex___state____state__sandbox_reflex___state_form____form_state.f_hotel_rx_state_},children)
    )
});
