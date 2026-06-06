
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Cond_comp_d258493e106f58c4c185e60c1413a726 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state_usuarios____usuario_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_usuarios____usuario_state)



    return(
        ((reflex___state____state__sandbox_reflex___state_usuarios____usuario_state.u_id_rx_state_?.valueOf?.() === -1?.valueOf?.())?(children?.at?.(0)):(children?.at?.(1)))
    )
});
