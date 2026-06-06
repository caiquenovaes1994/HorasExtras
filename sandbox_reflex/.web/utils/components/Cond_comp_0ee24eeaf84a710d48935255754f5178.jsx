
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Cond_comp_0ee24eeaf84a710d48935255754f5178 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state_hoteis____hotel_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_hoteis____hotel_state)



    return(
        ((reflex___state____state__sandbox_reflex___state_hoteis____hotel_state.solicitacoes_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
