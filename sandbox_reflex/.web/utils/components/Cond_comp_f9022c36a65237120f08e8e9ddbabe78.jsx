
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue,pyAnd} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Cond_comp_f9022c36a65237120f08e8e9ddbabe78 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state_hoteis____hotel_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_hoteis____hotel_state)
const reflex___state____state__sandbox_reflex___state____auth_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state)



    return(
        (pyAnd(((reflex___state____state__sandbox_reflex___state_hoteis____hotel_state.solicitacoes_rx_state_.length > 0) ? true : false), () => ((reflex___state____state__sandbox_reflex___state____auth_state.user_info_rx_state_?.["perfil"]?.valueOf?.() === "ADMIN"?.valueOf?.())))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
