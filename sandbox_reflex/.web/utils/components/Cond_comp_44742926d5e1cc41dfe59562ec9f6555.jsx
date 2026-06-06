
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Cond_comp_44742926d5e1cc41dfe59562ec9f6555 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state____auth_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state)



    return(
        (reflex___state____state__sandbox_reflex___state____auth_state.must_change_password_rx_state_?(children?.at?.(0)):(children?.at?.(1)))
    )
});
