
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Cond_comp_60a135de8c7e4a2024fd7179735feff4 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state____auth_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state)



    return(
        (reflex___state____state__sandbox_reflex___state____auth_state.show_policy_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
