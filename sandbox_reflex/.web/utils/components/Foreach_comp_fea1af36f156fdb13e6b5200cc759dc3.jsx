
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {StateContexts} from "$/utils/context"
import {Select as RadixThemesSelect} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Foreach_comp_fea1af36f156fdb13e6b5200cc759dc3 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state)



    return(
        Array.prototype.map.call(reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.opcoes_plantonistas_rx_state_ ?? [],((item_rx_state_,index_0d039201bc63b7e42b67c92685f4966c)=>(jsx(RadixThemesSelect.Item,{key:index_0d039201bc63b7e42b67c92685f4966c,value:item_rx_state_},item_rx_state_))))
    )
});
