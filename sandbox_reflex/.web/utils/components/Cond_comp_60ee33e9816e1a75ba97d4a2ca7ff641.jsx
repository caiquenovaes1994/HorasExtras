
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Cond_comp_60ee33e9816e1a75ba97d4a2ca7ff641 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state____auth_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state)



    return(
        (!((reflex___state____state__sandbox_reflex___state____auth_state.user_info_rx_state_?.["perfil"]?.valueOf?.() === "GESTOR"?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
