
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Bare_comp_300f59bc9e935a657c1674c8c9727e61 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state_usuarios____usuario_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_usuarios____usuario_state)



    return(
        ((reflex___state____state__sandbox_reflex___state_usuarios____usuario_state.u_id_rx_state_?.valueOf?.() === -1?.valueOf?.()) ? "Novo Usu\u00e1rio" : "Editar Usu\u00e1rio")
    )
});
