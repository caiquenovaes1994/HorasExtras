
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Cond_comp_c0630bb5a950f1327a41d187dcf9e958 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state____auth_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state)



    return(
        (!((reflex___state____state__sandbox_reflex___state____auth_state.user_info_rx_state_?.["perfil"]?.valueOf?.() === "USER"?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
