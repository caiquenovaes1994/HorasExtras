
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Cond_comp_e32567c8397acebbdb25f7009d753692 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state____auth_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state)



    return(
        (!((reflex___state____state__sandbox_reflex___state____auth_state.login_error_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
