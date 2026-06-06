
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Cond_comp_26deb490ff13214fbe09f2699d125b76 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state_form____form_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_form____form_state)



    return(
        (!(reflex___state____state__sandbox_reflex___state_form____form_state.is_view_only_rx_state_)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
