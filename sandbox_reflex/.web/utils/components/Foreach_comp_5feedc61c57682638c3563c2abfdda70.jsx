
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {Select as RadixThemesSelect} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Foreach_comp_5feedc61c57682638c3563c2abfdda70 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state_form____form_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_form____form_state)



    return(
        Array.prototype.map.call(reflex___state____state__sandbox_reflex___state_form____form_state.hoteis_opts_rx_state_ ?? [],((item_rx_state_,index_0d039201bc63b7e42b67c92685f4966c)=>(jsx(RadixThemesSelect.Item,{key:index_0d039201bc63b7e42b67c92685f4966c,value:item_rx_state_},item_rx_state_))))
    )
});
