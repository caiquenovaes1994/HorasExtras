
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Cond_comp_47e96c5e847b23cf6c766401e4b4a4af = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state)



    return(
        ((reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.selected_records_rx_state_.length > 0)?(children?.at?.(0)):(children?.at?.(1)))
    )
});
