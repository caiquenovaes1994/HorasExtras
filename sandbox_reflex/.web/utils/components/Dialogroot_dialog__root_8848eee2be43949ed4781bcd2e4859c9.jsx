
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {Dialog as RadixThemesDialog} from "@radix-ui/themes"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Dialogroot_dialog__root_8848eee2be43949ed4781bcd2e4859c9 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state_hoteis____hotel_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_hoteis____hotel_state)



    return(
        jsx(RadixThemesDialog.Root,{open:reflex___state____state__sandbox_reflex___state_hoteis____hotel_state.is_modal_open_rx_state_},children)
    )
});
