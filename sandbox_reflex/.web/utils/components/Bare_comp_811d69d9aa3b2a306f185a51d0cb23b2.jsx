
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Bare_comp_811d69d9aa3b2a306f185a51d0cb23b2 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state_form____form_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_form____form_state)



    return(
        ((reflex___state____state__sandbox_reflex___state_form____form_state.record_id_rx_state_?.valueOf?.() === -1?.valueOf?.()) ? "Inserir Novo Chamado" : (reflex___state____state__sandbox_reflex___state_form____form_state.is_view_only_rx_state_ ? "Visualizar Chamado" : "Editar Chamado"))
    )
});
