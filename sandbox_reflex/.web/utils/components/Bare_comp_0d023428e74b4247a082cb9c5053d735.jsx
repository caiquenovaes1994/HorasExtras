
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Bare_comp_0d023428e74b4247a082cb9c5053d735 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state)



    return(
        (reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.is_generating_pdf_rx_state_ ? "Processando Equipe..." : "Baixar Consolidado (Todos)")
    )
});
